import ActivityCalendar from "./activity-calendar"

interface DailyResult {
  date: string
  answer: string
  model: string
  correct: boolean
}

interface ModelAnswerBlockProps {
  modelName: string
  dailyResults: DailyResult[],
  startDate: string,
}

export default function ModelAnswerBlock({ modelName, dailyResults, startDate }: ModelAnswerBlockProps) {
  // Get the model version from the first result
  const modelVersion = dailyResults.length > 0 ? dailyResults[0].model : 'Unknown'

  // Find the first day the model reported a wrong answer (if any)
  const firstIncorrectDay = dailyResults.find((result) => !result.correct)
  
  // Format the date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden shadow-sm">
      <div className="bg-gray-100 p-4 border-b border-gray-300">
        <h3 className="text-xl font-serif font-bold capitalize">{modelName}</h3>
        <p className="text-sm text-gray-600 mt-1">Model: {modelVersion}</p>
      </div>

      <div className="p-4">
        {firstIncorrectDay && (
          <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-md">
            <p className="text-sm text-amber-800">
              <span className="font-medium">Model change detected:</span> On {formatDate(firstIncorrectDay.date)}, 
              the model gave an incorrect answer for the first time, responding with &quot;{firstIncorrectDay.answer}&quot;.
            </p>
          </div>
        )}

        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Daily Performance</h4>
          <ActivityCalendar dailyResults={dailyResults} startDate={startDate} />
        </div>
      </div>
    </div>
  )
}
