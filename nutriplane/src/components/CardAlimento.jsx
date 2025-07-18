export default function CardAlimento({ alimento }) {
  return (
    <div className="flex justify-between border-b py-1">
      <span>{alimento.nome}</span>
      <span>{alimento.quantidade}</span>
    </div>
  )
}
