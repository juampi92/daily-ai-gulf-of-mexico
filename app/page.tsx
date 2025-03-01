import QuestionSection from "@/components/question-section"
import ModelAnswerBlock from "@/components/model-answer-block"
import { getStaticModelData } from "@/lib/data"

// This ensures the page is statically generated at build time
export const dynamic = 'force-static';

export default function Home() {
  // Get the pre-computed data during build time
  const { modelResults, startDate } = getStaticModelData();
  
  // Format the build date for display
  const buildDate = new Date().toLocaleDateString();

  return (
    <main className="min-h-screen bg-stone-100 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <header className="border-b-2 border-black pb-4 mb-8">
          <h1 className="text-3xl font-serif font-bold text-center">THE DAILY AI OBSERVER</h1>
          <p className="text-center text-sm mt-2">Reporting AI model bias daily</p>
        </header>

        <QuestionSection />

        <section className="mt-16">
          <h2 className="text-2xl font-serif font-bold border-b-2 border-black pb-2 mb-6">
            MODEL PERFORMANCE TRACKING
          </h2>

          <div className="space-y-12">
            {modelResults.map((modelResult) => (
              <ModelAnswerBlock
                key={modelResult.model}
                modelName={modelResult.model}
                dailyResults={modelResult.dailyResults}
                startDate={startDate}
              />
            ))}
          </div>
        </section>

        <footer className="mt-16 pt-8 border-t border-gray-300 text-center text-sm text-gray-600">
          <p>Data last updated: {buildDate}</p>
        </footer>
      </div>
    </main>
  )
}
