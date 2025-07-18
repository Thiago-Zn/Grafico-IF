export default function DiaSelector() {
  const dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
  return (
    <div className="flex gap-2 p-2">
      {dias.map(d => (
        <button key={d} className="border px-2 py-1">{d}</button>
      ))}
    </div>
  )
}
