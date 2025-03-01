"use client"

import { useState, useEffect } from "react"

interface DailyResult {
  date: string
  answer: string
  model: string
  correct: boolean
}

interface ActivityCalendarProps {
  dailyResults: DailyResult[],
  startDate: string,
}

export default function ActivityCalendar({ dailyResults, startDate }: ActivityCalendarProps) {
  const [hoveredDay, setHoveredDay] = useState<DailyResult | null>(null)
  const [weeks, setWeeks] = useState<Array<Array<{date: string; result: DailyResult | null}>>>([])

  // Generate dates for a 4-month sliding window
  useEffect(() => {
    const generateCalendarDays = () => {
      // Use the build date as "today" to ensure consistency between builds
      const today = new Date()
      const days = []
      
      // Constants for window calculation
      const WINDOW_SIZE_MONTHS = 4
      const FUTURE_BUFFER_DAYS = 7 // 1 week empty in the future
      
      // Calculate window boundaries
      const calculateWindowBoundaries = (): { windowStart: Date; windowEnd: Date } => {
        // Initialize with the original start date adjusted to Monday
        const dataStartDate = new Date(startDate)
        
        // Adjust to previous Monday
        const adjustToMonday = (date: Date): Date => {
          const dayOfWeek = date.getDay() // 0 = Sunday, 1 = Monday, ...
          if (dayOfWeek !== 1) {
            // If Sunday (0), go back 6 days; if Tuesday (2), go back 1 day, etc.
            const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1
            date.setDate(date.getDate() - daysToSubtract)
          }
          return date
        }
        
        // Adjust to next Sunday
        const adjustToSunday = (date: Date): Date => {
          const dayOfWeek = date.getDay() // 0 = Sunday
          if (dayOfWeek !== 0) {
            const daysToAdd = 7 - dayOfWeek
            date.setDate(date.getDate() + daysToAdd)
          }
          return date
        }
        
        // Adjust data start date to previous Monday
        const windowStartBase = adjustToMonday(new Date(dataStartDate))
        
        // Calculate the ideal end date (today minus future buffer)
        const idealEndDate = new Date(today)
        idealEndDate.setDate(idealEndDate.getDate() - FUTURE_BUFFER_DAYS)
        
        // Calculate the minimum window end date (start date + window size)
        const minWindowEndDate = new Date(windowStartBase)
        minWindowEndDate.setMonth(minWindowEndDate.getMonth() + WINDOW_SIZE_MONTHS)
        
        // Determine the actual window end date (the later of the two options)
        const windowEndBase = minWindowEndDate.getTime() > idealEndDate.getTime() 
          ? new Date(minWindowEndDate.getTime()) 
          : new Date(idealEndDate.getTime())
        
        // If we have more data than fits in the window, slide the window
        let windowStart: Date
        // Approximate 4 months in milliseconds (4 months * 30 days * 24 hours * 60 minutes * 60 seconds * 1000 ms)
        const fourMonthsInMs = WINDOW_SIZE_MONTHS * 30 * 24 * 60 * 60 * 1000
        if (windowEndBase.getTime() - windowStartBase.getTime() > fourMonthsInMs) {
          // Calculate how far to slide the window
          windowStart = new Date(windowEndBase)
          windowStart.setMonth(windowStart.getMonth() - WINDOW_SIZE_MONTHS)
          windowStart = adjustToMonday(windowStart)
        } else {
          // Not enough data to fill window, use original start
          windowStart = windowStartBase
        }
        
        // Adjust window end to next Sunday
        const windowEnd = adjustToSunday(new Date(windowEndBase))
        
        return { windowStart, windowEnd }
      }
      
      // Get window boundaries
      const { windowStart, windowEnd } = calculateWindowBoundaries()
      
      // Use these as our current date and calendar end date
      const currentDate = new Date(windowStart)
      const calendarEndDate = windowEnd

      // Create a map of results by date for quick lookup
      const resultsByDate = new Map()
      dailyResults.forEach((result) => {
        resultsByDate.set(result.date, result)
      })

      while (currentDate <= calendarEndDate) {
        const dateString = currentDate.toISOString().split("T")[0]
        const result = resultsByDate.get(dateString)

        days.push({
          date: dateString,
          result: result || null,
        })

        // Move to next day
        currentDate.setDate(currentDate.getDate() + 1)
      }

      return days
    }

    const days = generateCalendarDays()
    
    // Group days by week for display
    const weekGroups = []
    for (let i = 0; i < days.length; i += 7) {
      weekGroups.push(days.slice(i, i + 7))
    }
    setWeeks(weekGroups)
  }, [dailyResults, startDate])

  // Get color for a day based on result
  const getDayColor = (day: { date: string; result: DailyResult | null }) => {
    if (!day.result) return "bg-gray-200" // No data
    return day.result.correct ? "bg-green-500" : "bg-red-500"
  }

  // Get cursor style based on whether day has data
  const getCursorStyle = (day: { date: string; result: DailyResult | null }) => {
    return day.result ? "cursor-pointer" : "cursor-default"
  }

  // State to track mouse position for tooltip
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  // Handle mouse move to update position
  const handleMouseMove = (e: React.MouseEvent) => {
    setMousePosition({ x: e.clientX, y: e.clientY })
  }

  const calendarStyle = {
    maxWidth: '800px', // Set a maximum width
    margin: '0 auto',  // Center the calendar
    width: '100%',     // Allow it to take full width up to max-width
  };

  return (
    <div style={calendarStyle} className="relative" onMouseMove={handleMouseMove}>
      <div className="flex flex-wrap gap-1">
        {weeks.map((week, weekIndex) => (
          <div key={weekIndex} className="flex flex-col gap-1">
            {week.map((day) => (
              <div
                key={day.date}
                className={`w-3 h-3 rounded-sm ${getDayColor(day)} ${getCursorStyle(day)}`}
                onMouseEnter={() => day.result && setHoveredDay(day.result)}
                onMouseLeave={() => setHoveredDay(null)}
              />
            ))}
          </div>
        ))}
      </div>

      {hoveredDay && (
        <div 
          className="fixed bg-white border border-gray-200 rounded p-2 shadow-lg z-50 text-sm"
          style={{ 
            left: `${mousePosition.x + 10}px`, 
            top: `${mousePosition.y - 10}px` 
          }}
        >
          <p>
            <strong>Date:</strong> {hoveredDay.date}
          </p>
          <p>
            <strong>Answer:</strong> {hoveredDay.answer}
          </p>
          <p>
            <strong>Model:</strong> {hoveredDay.model}
          </p>
          <p>
            <strong>Status:</strong> {hoveredDay.correct ? "Correct" : "Incorrect"}
          </p>
        </div>
      )}

      <div className="flex items-center gap-4 mt-2 text-xs text-gray-600">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-gray-200 rounded-sm"></div>
          <span>No data</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded-sm"></div>
          <span>Correct</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-red-500 rounded-sm"></div>
          <span>Incorrect</span>
        </div>
      </div>
    </div>
  )
}
