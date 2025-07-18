export function calcularMacros(alimentos) {
  return alimentos.reduce(
    (totais, item) => {
      return {
        calorias: totais.calorias + (item.calorias || 0),
        proteina: totais.proteina + (item.proteina || 0),
        carboidrato: totais.carboidrato + (item.carboidrato || 0),
        gordura: totais.gordura + (item.gordura || 0)
      }
    },
    { calorias: 0, proteina: 0, carboidrato: 0, gordura: 0 }
  )
}
