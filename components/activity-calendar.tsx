"use client"

import { useMemo, useEffect, useRef } from "react"
import { generateCalendarDays, groupDaysByWeek } from "@/lib/date-utils"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

interface DailyResult {
  date: string
  answer: string
  model: string
  correct: boolean
}

interface ActivityCalendarProps {
  dailyResults: DailyResult[]
  startDate: string
}

// Constants for styling
const DAY_SIZE = "w-3 h-3"
const GAP_SIZE = "gap-1"

export default function ActivityCalendar({ dailyResults, startDate }: ActivityCalendarProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  // Generate calendar days using memoization for performance
  const days = useMemo(
    () => generateCalendarDays(startDate, dailyResults),
    [startDate, dailyResults]
  )

  // Group days by week
  const weeks = useMemo(() => groupDaysByWeek(days), [days])

  // Auto-scroll to the right (most recent) on mount
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = scrollRef.current.scrollWidth
    }
  }, [weeks])

  // Get color for a day based on result
  const getDayColor = (day: { date: string; result: DailyResult | null }) => {
    if (!day.result) return "bg-gray-200" // No data
    return day.result.correct ? "bg-green-500" : "bg-red-500"
  }

  // Get cursor style based on whether day has data
  const getCursorStyle = (day: { date: string; result: DailyResult | null }) => {
    return day.result ? "cursor-pointer" : "cursor-default"
  }

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  return (
    <div className="max-w-[800px] mx-auto w-full">
      <div 
        ref={scrollRef}
        className={`overflow-x-auto flex ${GAP_SIZE} pb-2`}
      >
        <TooltipProvider delayDuration={0} skipDelayDuration={300}>
          {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className={`flex flex-col ${GAP_SIZE}`}>
              {week.map((day) => {
                const hasData = !!day.result

                if (!hasData) {
                  return (
                    <div
                      key={day.date}
                      className={`${DAY_SIZE} rounded-sm bg-gray-200 ${getCursorStyle(day)}`}
                      title={formatDate(day.date)}
                    >
                      <span className="text-xs text-gray-500"></span>
                    </div>
                  )
                }
                
                 return (
                   <Tooltip key={day.date} disableHoverableContent>
                     <TooltipTrigger asChild>
                       <div
                         className={`${DAY_SIZE} rounded-sm ${getDayColor(day)} ${getCursorStyle(day)}`}
                         // role={hasData ? "button" : undefined}
                         tabIndex={hasData ? 0 : -1}
                         aria-label={`${formatDate(day.date)}: ${day.result!.correct ? 'Correct' : 'Incorrect'}`}
                       />
                     </TooltipTrigger>
                     <TooltipContent side="top" className="max-w-xs">
                       <div className="space-y-1">
                         <p>
                           <strong>Date:</strong> {formatDate(day.date)}
                         </p>
                         <p>
                           <strong>Answer:</strong> {day.result!.answer}
                         </p>
                         <p>
                           <strong>Model:</strong> {day.result!.model}
                         </p>
                         <p>
                           <strong>Status:</strong>{" "}
                           {day.result!.correct ? "Correct" : "Incorrect"}
                         </p>
                       </div>
                     </TooltipContent>
                  </Tooltip>
                )
              })}
            </div>
          ))}
        </TooltipProvider>
      </div>

      <div className={`flex items-center ${GAP_SIZE} gap-4 mt-2 text-xs text-gray-600`}>
        <div className="flex items-center gap-1">
          <div className={`${DAY_SIZE} bg-gray-200 rounded-sm`}></div>
          <span>No data</span>
        </div>
        <div className="flex items-center gap-1">
          <div className={`${DAY_SIZE} bg-green-500 rounded-sm`}></div>
          <span>Correct</span>
        </div>
        <div className="flex items-center gap-1">
          <div className={`${DAY_SIZE} bg-red-500 rounded-sm`}></div>
          <span>Incorrect</span>
        </div>
      </div>
    </div>
  )
}
