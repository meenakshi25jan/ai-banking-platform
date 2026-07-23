export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold">About Our Institute</h1>
      <p className="mt-6 text-lg text-gray-600 dark:text-gray-400">
        We are a leading educational institution committed to academic excellence,
        innovation, and holistic student development. Our admission platform
        streamlines the entire enrollment process for students and parents.
      </p>
      <div className="mt-12 grid gap-6 sm:grid-cols-3">
        {[
          { label: 'Students Enrolled', value: '10,000+' },
          { label: 'Courses Offered', value: '50+' },
          { label: 'Departments', value: '12' },
        ].map((s) => (
          <div key={s.label} className="card text-center">
            <div className="text-3xl font-bold text-brand-600">{s.value}</div>
            <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">{s.label}</div>
          </div>
        ))}
      </div>
      <h2 className="mt-12 text-2xl font-bold">Our Mission</h2>
      <p className="mt-4 text-gray-600 dark:text-gray-400">
        To provide accessible, transparent, and efficient admission services
        that empower every student to pursue their educational goals.
      </p>
    </div>
  );
}
