import { NavLink } from 'react-router-dom'

const linkClass = ({ isActive }) =>
  `px-3 py-2 ${isActive ? 'font-bold text-blue-600' : 'text-gray-600'}`

export default function Header() {
  return (
    <header className="bg-white border-b shadow-sm">
      <nav className="container mx-auto flex gap-4 p-4 text-sm">
        <NavLink to="/planejamento" className={linkClass}>Planejamento</NavLink>
        <NavLink to="/compras" className={linkClass}>Compras</NavLink>
        <NavLink to="/resumo" className={linkClass}>Resumo</NavLink>
        <NavLink to="/importar" className={linkClass}>Importar</NavLink>
      </nav>
    </header>
  )
}
