import { useState, useEffect, useRef } from 'react'

const BAR_COUNT = 24
const SMOOTHING = 0.25
const MIN_HEIGHT = 0.06
const FFT_SIZE = 512
const GAIN = 7.5

function MicrophoneInput({ isActive = true }) {
  const [barHeights, setBarHeights] = useState(() =>
    Array.from({ length: BAR_COUNT }, () => MIN_HEIGHT)
  )
  const smoothedRef = useRef(Array.from({ length: BAR_COUNT }, () => MIN_HEIGHT))
  const streamRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const rafRef = useRef(null)

  useEffect(() => {
    if (!isActive) {
      setBarHeights(Array.from({ length: BAR_COUNT }, () => MIN_HEIGHT))
      smoothedRef.current = Array.from({ length: BAR_COUNT }, () => MIN_HEIGHT)
      return
    }

    let cancelled = false

    const init = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop())
          return
        }
        streamRef.current = stream

        const AudioContextClass = window.AudioContext || window.webkitAudioContext
        const audioContext = new AudioContextClass()
        audioContextRef.current = audioContext
        if (audioContext.state === 'suspended') {
          await audioContext.resume()
        }
        if (cancelled) return

        const analyser = audioContext.createAnalyser()
        analyser.fftSize = FFT_SIZE
        analyser.smoothingTimeConstant = 0.7
        analyser.minDecibels = -60
        analyser.maxDecibels = -10
        analyserRef.current = analyser

        const source = audioContext.createMediaStreamSource(stream)
        source.connect(analyser)

        const dataArray = new Uint8Array(analyser.frequencyBinCount)
        const bins = analyser.frequencyBinCount
        const step = Math.max(1, Math.floor(bins / BAR_COUNT))

        const update = () => {
          if (cancelled || !analyserRef.current) return
          analyser.getByteFrequencyData(dataArray)
          const next = [...smoothedRef.current]
          for (let i = 0; i < BAR_COUNT; i++) {
            let sum = 0
            const start = i * step
            const end = Math.min(start + step, bins)
            for (let j = start; j < end; j++) sum += dataArray[j]
            const avg = (sum / (end - start)) / 255
            const target = MIN_HEIGHT + (1 - MIN_HEIGHT) * Math.min(1, avg * GAIN)
            next[i] = smoothedRef.current[i] + (target - smoothedRef.current[i]) * (1 - SMOOTHING)
          }
          smoothedRef.current = next
          setBarHeights(next)
          rafRef.current = requestAnimationFrame(update)
        }
        rafRef.current = requestAnimationFrame(update)
      } catch (err) {
        if (!cancelled) setBarHeights(Array.from({ length: BAR_COUNT }, () => MIN_HEIGHT))
      }
    }

    init()
    return () => {
      cancelled = true
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
      rafRef.current = null
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop())
        streamRef.current = null
      }
      if (audioContextRef.current) {
        audioContextRef.current.close().catch(() => {})
        audioContextRef.current = null
      }
      analyserRef.current = null
    }
  }, [isActive])

  return (
    <div className="pt-2 border-t border-slate-100">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-slate-400">Microphone Active</span>
        {isActive && (
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-green-500">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" aria-hidden="true" />
            Live Input
          </span>
        )}
      </div>
      <div
        className="flex items-end justify-center gap-[2px] sm:gap-[3px] md:gap-1 h-7 sm:h-8 md:h-10"
        role="img"
        aria-label="Audio level visualization"
      >
        {barHeights.map((height, i) => (
          <div
            key={i}
            className="w-1 sm:w-1.5 md:w-[7px] min-h-1 rounded-sm bg-blue-600 ease-out"
            style={{
              height: `${Math.max(MIN_HEIGHT * 100, height * 100)}%`,
              transition: 'height 0.12s ease-out',
            }}
          />
        ))}
      </div>
    </div>
  )
}

export default MicrophoneInput
