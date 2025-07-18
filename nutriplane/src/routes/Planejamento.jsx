import DiaSelector from '../components/DiaSelector'
import CardRefeicao from '../components/CardRefeicao'

export default function Planejamento() {
  return (
    <div>
      <DiaSelector />
      <div className="mt-4 space-y-4">
        <CardRefeicao nome="Café da manhã" />
        <CardRefeicao nome="Almoço" />
        <CardRefeicao nome="Jantar" />
      </div>
    </div>
  )
}
