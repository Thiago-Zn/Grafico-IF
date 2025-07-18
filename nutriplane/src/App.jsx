import { Routes, Route, Navigate } from 'react-router-dom'
import Home from './routes/Home'
import Planejamento from './routes/Planejamento'
import ListaCompras from './routes/ListaCompras'
import ResumoMacros from './routes/ResumoMacros'
import ImportadorPlanilha from './routes/ImportadorPlanilha'
import Header from './components/Header'

export default function App() {
  return (
    <div className="min-h-screen">
      <Header />
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Navigate to="/planejamento" />} />
          <Route path="/home" element={<Home />} />
          <Route path="/planejamento" element={<Planejamento />} />
          <Route path="/compras" element={<ListaCompras />} />
          <Route path="/resumo" element={<ResumoMacros />} />
          <Route path="/importar" element={<ImportadorPlanilha />} />
        </Routes>
      </main>
    </div>
  )
}
