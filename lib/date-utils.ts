interface DailyResult {
  date: string
  answer: string
  model: string
  correct: boolean
}

/**
 * Adjusts a date to the previous Monday
 * If already Monday, returns the same date
 */
export function adjustToMonday(date: Date): Date {
  const newDate = new Date(date)
  const dayOfWeek = newDate.getDay() // 0 = Sunday, 1 = Monday, ...
  if (dayOfWeek !== 1) {
    // If Sunday (0), go back 6 days; if Tuesday (2), go back 1 day, etc.
    const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1
    newDate.setDate(newDate.getDate() - daysToSubtract)
  }
  return newDate
}

/**
 * Adjusts a date to the next Sunday
 * If already Sunday, returns the same date
 */
export function adjustToSunday(date: Date): Date {
  const newDate = new Date(date)
  const dayOfWeek = newDate.getDay() // 0 = Sunday
  if (dayOfWeek !== 0) {
    const daysToAdd = 7 - dayOfWeek
    newDate.setDate(newDate.getDate() + daysToAdd)
  }
  return newDate
}

/**
 * Generates calendar days from start date to today (no future dates)
 * Returns an array of day objects with dates and associated results
 */
export function generateCalendarDays(
  startDate: string,
  dailyResults: DailyResult[]
): Array<{ date: string; result: DailyResult | null }> {
  const days: Array<{ date: string; result: DailyResult | null }> = []
  
  // Parse the start date and adjust to previous Monday
  const dataStartDate = new Date(startDate)
  const currentDate = adjustToMonday(new Date(dataStartDate))
  
  // Calculate end date: today (no future dates)
  const today = new Date()
  // Set time to end of day to include today
  today.setHours(23, 59, 59, 999)
  
  // Create a map of results by date for quick lookup
  const resultsByDate = new Map<string, DailyResult>()
  dailyResults.forEach((result) => {
    resultsByDate.set(result.date, result)
  })
  
  // Generate all days from start to today only
  while (currentDate <= today) {
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

/**
 * Groups an array of days into weeks (7 days per week)
 */
export function groupDaysByWeek<T>(days: T[]): T[][] {
  const weeks: T[][] = []
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7))
  }
  return weeks
}

