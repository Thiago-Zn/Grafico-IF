export default function CardAlimento({ nome, quantidade }) {
  return (
    <div className="flex justify-between border-b py-1">
      <span>{nome}</span>
      <span className="text-sm text-gray-500">{quantidade}</span>
    </div>
  )
}
