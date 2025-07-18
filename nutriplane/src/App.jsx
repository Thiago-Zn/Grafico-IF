import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './routes/Home'
import Planejamento from './routes/Planejamento'
import ListaCompras from './routes/ListaCompras'
import ResumoMacros from './routes/ResumoMacros'
import ImportadorPlanilha from './routes/ImportadorPlanilha'

export default function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/planejamento" element={<Planejamento />} />
        <Route path="/compras" element={<ListaCompras />} />
        <Route path="/resumo" element={<ResumoMacros />} />
        <Route path="/importar" element={<ImportadorPlanilha />} />
      </Routes>
    </Router>
  )
}
