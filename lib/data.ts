import fs from "fs"
import path from "path"
import { parse } from "csv-parse/sync"

export interface ModelData {
  model: string
  date: string
  answer: string
  correct: boolean | string
}

export interface ModelResults {
  model: string
  dailyResults: {
    date: string
    answer: string
    model: string
    correct: boolean
  }[]
}

// This function will be used during static site generation
export function getStaticModelData(): {
  modelResults: ModelResults[];
  startDate: string;
} {
  const modelResults = getAllModelData();
  const startDate = findEarliestDate(modelResults);
  
  return {
    modelResults,
    startDate: startDate.toISOString().split("T")[0],
  };
}

export function getModelData(modelName: string): ModelResults | null {
  try {
    const dataDir = path.join(process.cwd(), "public/data")
    const filePath = path.join(dataDir, `${modelName}.csv`)

    // Check if file exists
    if (!fs.existsSync(filePath)) {
      console.warn(`File ${modelName}.csv does not exist.`)
      return null
    }

    const fileContent = fs.readFileSync(filePath, "utf8")
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
    }) as ModelData[]

    // Process records and stop at first incorrect answer
    const dailyResults = []
    let stopProcessing = false

    for (const record of records) {
      if (stopProcessing) break

      // Create the result object with required fields
      const resultObj: {
        date: string;
        answer: string;
        model: string;
        correct: boolean;
      } = {
        date: record.date,
        answer: record.answer,
        model: record.model || modelName, // Use the model field from the record or fallback to modelName
        correct: typeof record.correct === "string" ? record.correct.toLowerCase().trim() === "true" : Boolean(record.correct),
      }
      
      dailyResults.push(resultObj)

      if (!record.correct) {
        stopProcessing = true
      }
    }

    return {
      model: modelName,
      dailyResults,
    }
  } catch (error) {
    console.error(`Error processing ${modelName}.csv:`, error)
    return null
  }
}

export function getAllModelData(): ModelResults[] {
  const modelNames = ["openai", "anthropic", "google", "xai"]
  const results: ModelResults[] = []

  for (const modelName of modelNames) {
    const modelData = getModelData(modelName)
    if (modelData) {
      results.push(modelData)
    }
  }

  return results
}

// Function to find the earliest date in the model results
export function findEarliestDate(modelResults: ModelResults[]): Date {
  if (!modelResults.length || !modelResults[0].dailyResults.length) {
    return new Date();
  }
  
  // StartDate must be the smallest initial date in the data
  let startDate = new Date(modelResults[0].dailyResults[0].date)
  for (const modelResult of modelResults) {
    for (const dailyResult of modelResult.dailyResults) {
      const currentDate = new Date(dailyResult.date)
      if (currentDate < startDate) {
        startDate = currentDate
      }
    }
  }
  return startDate
}
