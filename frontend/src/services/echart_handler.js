class EchartsHandler {
    /**
     * Create empty chart option when no data is available
     * @returns {Object} Empty ECharts option
     */
    createEmptyChartOption() {
        return {
            title: {
                text: 'Histórico de Potência Ativa',
                subtext: 'Nenhum dado disponível',
                left: 'center'
            },
            xAxis: {
                type: 'category',
                data: []
            },
            yAxis: {
                type: 'value',
                name: 'Potência (MW)'
            },
            series: []
        }
    }
}

export default new EchartsHandler();