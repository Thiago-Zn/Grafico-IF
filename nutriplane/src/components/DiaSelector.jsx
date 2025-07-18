import { useState } from 'react'

const dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

export default function DiaSelector() {
  const [dia, setDia] = useState(0)

  return (
    <div className="flex gap-2">
      {dias.map((d, i) => (
        <button
          key={d}
          onClick={() => setDia(i)}
          className={`px-2 py-1 rounded ${dia === i ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          {d}
        </button>
      ))}
    </div>
  )
}
