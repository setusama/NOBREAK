from flask import Flask, render_template, request

app = Flask(__name__)

# Função para calcular a capacidade da bateria em kVA
def calcular_bateria_kva(watts, fator_potencia, horas_autonomia, fator_folga):
    folga = 1 + (fator_folga / 100)  # Aplicando o fator de folga
    consumo_total = watts * folga  # Consumo total com folga aplicada
    capacidade_bateria_vah = (consumo_total * horas_autonomia) / fator_potencia  # Cálculo da capacidade da bateria em VAh
    capacidade_bateria_kva = capacidade_bateria_vah / 1000  # Converter de VAh para kVA
    
    return capacidade_bateria_kva

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    valores = {
        "watts": "",
        "fator_potencia": "",
        "horas_autonomia": "",
        "fator_folga": "",
        "forma_onda": ""
    }
    
    if request.method == 'POST':
        watts = float(request.form['watts'])
        fator_potencia = float(request.form['fator_potencia'])
        horas_autonomia = float(request.form['horas_autonomia'])
        forma_onda = request.form['forma_onda']
        fator_folga = float(request.form['fator_folga'])

        # Calcular capacidade da bateria necessária em kVA
        capacidade_bateria_kva = calcular_bateria_kva(watts, fator_potencia, horas_autonomia, fator_folga)
        resultado = f"A capacidade mínima da bateria necessária é: {capacidade_bateria_kva:.2f} kVAh"

        # Guardar os valores preenchidos
        valores = {
            "watts": watts,
            "fator_potencia": fator_potencia,
            "horas_autonomia": horas_autonomia,
            "fator_folga": fator_folga,
            "forma_onda": forma_onda
        }
    
    return render_template('index.html', resultado=resultado, valores=valores)

if __name__ == '__main__':
    app.run(debug=True)
