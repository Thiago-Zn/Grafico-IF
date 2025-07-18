export function calcularMacros(alimentos) {
  return alimentos.reduce(
    (totais, item) => {
      return {
        calorias: totais.calorias + item.calorias,
        proteina: totais.proteina + item.proteina,
        carboidrato: totais.carboidrato + item.carboidrato,
        gordura: totais.gordura + item.gordura,
      }
    },
    { calorias: 0, proteina: 0, carboidrato: 0, gordura: 0 }
  )
}
