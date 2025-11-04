import {ref} from "vue";

class Api_utils {
    async dataProcessMap(response) {
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
        const stateData = ref([])

        if (response && response.result_code === '1' && response.result_data) {
            stateData.value = response.result_data.map(item => {
                const stateName = codeToStateName[item] || `Estado ${item.code}`
                return {
                    name: stateName,
                    activePower: item.state_realtime_power,
                    totalPower: item.state_installed_power
                }
            })
            console.log('Valores carregados com sucesso: ', stateData.value.length, ' estados processados.');
        }
    }
}