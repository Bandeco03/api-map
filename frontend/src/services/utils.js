class PowerDataManagement {
    formatPower(power) {
        // Convert to GW if > 1000 MW, otherwise show in MW
        if (power >= 1000000000) {
            return `${(power / 1000000000).toFixed(2)} GW`
        } else if (power >= 1000000) {
            return `${(power / 1000000).toFixed(2)} MW`
        } else if (power >= 1000) {
            return `${(power / 1000).toFixed(2)} kW`
        } else {
            return `${power.toFixed(2)} W`
        }
    }
}

export default new PowerDataManagement()