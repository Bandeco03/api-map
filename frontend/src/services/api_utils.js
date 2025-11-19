class ApiUtils {
    dataProcessMap(response) {
        const codeToStateName = {
            '12': 'Acre',
            '27': 'Alagoas',
            '16': 'Amapá',
            '13': 'Amazonas',
            '29': 'Bahia',
            '23': 'Ceará',
            '32': 'Espírito Santo',
            '52': 'Goiás',
            '21': 'Maranhão',
            '51': 'Mato Grosso',
            '50': 'Mato Grosso do Sul',
            '31': 'Minas Gerais',
            '15': 'Pará',
            '25': 'Paraíba',
            '41': 'Paraná',
            '26': 'Pernambuco',
            '22': 'Piauí',
            '33': 'Rio de Janeiro',
            '24': 'Rio Grande do Norte',
            '43': 'Rio Grande do Sul',
            '11': 'Rondônia',
            '14': 'Roraima',
            '42': 'Santa Catarina',
            '35': 'São Paulo',
            '28': 'Sergipe',
            '17': 'Tocantins',
            '53': 'Distrito Federal'
        }

        if (response && response.result_code === '1' && response.result_data) {
            const totals = this.dataProcessSum(response)
            const processedData = response.result_data.map(item => {
                const stateName = codeToStateName[item.code] || `Estado ${item.code}`
                return {
                    name: stateName,
                    value: item.state_realtime_power / 1000000, // Convert to MW for visualMap
                    activePower: item.state_realtime_power,
                    totalPower: item.state_installed_power,
                    activePowerRate: (item.state_realtime_power / totals.totalActivePower) * 100
                }
            })
            console.log('Valores carregados com sucesso: ', processedData.length, ' estados processados.');
            return processedData
        }

        return []
    }

    /**
     * Process historical power data
     * @param {Array} historyData - Array of historical records from the database
     * @returns {Object} Processed data with timestamps and power values
     */
    dataProcessHistory(historyData) {
        if (!historyData || !Array.isArray(historyData) || historyData.length === 0) {
            return {
                timestamps: [],
                activePower: []
            }
        }

        // Sort by timestamp (oldest first for chronological order)
        const sortedData = [...historyData].sort((a, b) =>
            new Date(a.timestamp) - new Date(b.timestamp)
        )

        const timestamps = []
        const activePowerValues = []

        sortedData.forEach(record => {
            if (record.data && record.data.result_code === '1' && record.data.result_data) {
                // Calculate total active power for this timestamp
                const totalActivePower = record.data.result_data.reduce((sum, item) => {
                    return sum + (item.state_realtime_power || 0)
                }, 0)

                // Format timestamp for display
                const date = new Date(record.timestamp)
                const formattedTime = date.toLocaleString('pt-BR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })

                timestamps.push(formattedTime)
                // Convert to MW for better readability
                activePowerValues.push((totalActivePower / 1000000).toFixed(2))
            }
        })

        return {
            timestamps,
            activePower: activePowerValues
        }
    }

    dataProcessSum(response) {
        if (response && response.result_code === '1' && response.result_data) {
            let totalActivePower = 0
            let totalInstalledPower = 0

            response.result_data.forEach(item => {
                totalActivePower += item.state_realtime_power
                totalInstalledPower += item.state_installed_power
            })

            return {
                totalActivePower,
                totalInstalledPower
            }
        }
    }
}

export default new ApiUtils();
