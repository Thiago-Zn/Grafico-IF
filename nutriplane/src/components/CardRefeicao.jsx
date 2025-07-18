export default function CardRefeicao({ titulo, children }) {
  return (
    <div className="border p-2 mb-2">
      <h2 className="font-bold mb-2">{titulo}</h2>
      {children}
    </div>
  )
}
