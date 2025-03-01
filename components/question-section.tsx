export default function QuestionSection() {
  return (
    <section className="mb-12">
      <div className="border-b-2 border-black pb-4">
        <h2 className="text-4xl font-serif font-bold leading-tight">
          What is the gulf between America and Mexico called?
        </h2>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 border border-green-600 bg-green-50 rounded-md">
          <h3 className="text-xl font-serif font-bold mb-2 flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 mr-2 text-green-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Correct Answer
          </h3>
          <p className="text-2xl font-medium">Gulf of Mexico</p>
          <p className="mt-2 text-sm text-gray-600">
            The Gulf of Mexico is an ocean basin and a marginal sea of the Atlantic Ocean, largely surrounded by the
            North American continent.
          </p>
        </div>

        <div className="p-6 border border-red-600 bg-red-50 rounded-md">
          <h3 className="text-xl font-serif font-bold mb-2 flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 mr-2 text-red-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
            Incorrect Answer
          </h3>
          <p className="text-2xl font-medium">Gulf of America</p>
          <p className="mt-2 text-sm text-gray-600">
            This is not the correct name. There is no body of water officially named the &quot;Gulf of America&quot;.
          </p>
        </div>
      </div>
    </section>
  )
}

