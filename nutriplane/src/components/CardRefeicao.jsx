export default function CardRefeicao({ nome }) {
  return (
    <div className="border rounded p-4 shadow-sm bg-white">
      <header className="font-semibold mb-2">{nome}</header>
      <p className="text-gray-600 text-sm">Adicione alimentos aqui.</p>
    </div>
  )
}
