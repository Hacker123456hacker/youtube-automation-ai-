import { FormEvent, useState } from 'react'

type ScriptResult = {
  topic: string
  language: string
  title: string
  script: string
  estimated_duration_minutes: number
}

export default function App() {
  const [topic, setTopic] = useState('')
  const [language, setLanguage] = useState('Hindi')
  const [duration, setDuration] = useState(3)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<ScriptResult | null>(null)

  async function generateScript(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const response = await fetch('/api/content/generate-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, language, duration_minutes: duration }),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Script generation failed. Please try again.')
      }
      setResult(data as ScriptResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not connect to the backend.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-8">
      <div className="mx-auto max-w-4xl">
        <header className="mb-10">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-cyan-300">Creator Studio · MVP</p>
          <h1 className="text-4xl font-black tracking-tight sm:text-5xl">YouTube Automation AI</h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-300">
            Generate a narration-ready video script from a topic. Voice generation, MP4 rendering and YouTube uploads are not connected yet.
          </p>
        </header>

        <section className="rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-2xl sm:p-8">
          <h2 className="text-2xl font-bold">Create a video script</h2>
          <p className="mt-2 text-sm text-slate-400">Add your OpenAI API key to backend/.env before using this feature.</p>
          <form onSubmit={generateScript} className="mt-6 space-y-5">
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-200">Video topic</span>
              <input
                required
                minLength={3}
                maxLength={300}
                value={topic}
                onChange={(event) => setTopic(event.target.value)}
                placeholder="उदाहरण: 2026 के 5 उपयोगी AI tools"
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
              />
            </label>
            <div className="grid gap-5 sm:grid-cols-2">
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-200">Script language</span>
                <select value={language} onChange={(event) => setLanguage(event.target.value)} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3">
                  <option>Hindi</option>
                  <option>Hinglish</option>
                  <option>English</option>
                </select>
              </label>
              <label className="block">
                <span className="mb-2 block text-sm font-medium text-slate-200">Target duration</span>
                <select value={duration} onChange={(event) => setDuration(Number(event.target.value))} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3">
                  <option value={1}>1 minute</option>
                  <option value={3}>3 minutes</option>
                  <option value={5}>5 minutes</option>
                  <option value={10}>10 minutes</option>
                  <option value={15}>15 minutes</option>
                  <option value={20}>20 minutes</option>
                </select>
              </label>
            </div>
            <button disabled={loading} type="submit" className="w-full rounded-xl bg-cyan-400 px-5 py-3.5 font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60">
              {loading ? 'Generating script…' : 'Generate AI script'}
            </button>
          </form>
          {error && <p role="alert" className="mt-5 rounded-xl border border-rose-700 bg-rose-950/50 p-4 text-rose-200">{error}</p>}
        </section>

        {result && (
          <section className="mt-8 rounded-3xl border border-slate-700 bg-slate-900 p-6 sm:p-8">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-sm text-cyan-300">Generated script</p>
                <h2 className="mt-1 text-2xl font-bold">{result.title}</h2>
              </div>
              <button type="button" onClick={() => navigator.clipboard.writeText(result.script)} className="rounded-lg border border-slate-600 px-3 py-2 text-sm hover:border-cyan-300">Copy script</button>
            </div>
            <p className="mt-3 text-sm text-slate-400">{result.language} · approximately {result.estimated_duration_minutes} minutes</p>
            <pre className="mt-5 whitespace-pre-wrap break-words font-sans leading-7 text-slate-200">{result.script}</pre>
          </section>
        )}

        <footer className="mt-8 text-sm text-slate-500">
          Never put API keys in frontend code. Configure secrets only on the backend.
        </footer>
      </div>
    </main>
  )
}
