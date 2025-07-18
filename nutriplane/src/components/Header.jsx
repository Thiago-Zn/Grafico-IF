import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="p-4 bg-blue-500 text-white flex gap-4">
      <Link to="/">Home</Link>
      <Link to="/planejamento">Planejamento</Link>
      <Link to="/compras">Compras</Link>
      <Link to="/resumo">Resumo</Link>
      <Link to="/importar">Importar</Link>
    </header>
  )
}
