document.addEventListener("DOMContentLoaded", () => {
    // Extract data from the global `salesData` variable
    const labels = salesData.map(sale => sale.Month);
    const policyCountData = salesData.map(sale => sale.Policy_Count);
    const premiumData = salesData.map(sale => sale.Total_Premium);

    // Initialize chart with Policy Count as default
    const ctx = document.getElementById("salesChart").getContext("2d");
    const salesChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Monthly Policy Count",
                    data: policyCountData,
                    backgroundColor: "rgba(0, 123, 255, 0.3)",
                    borderColor: "rgba(0, 123, 255, 1)",
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // Hide legend since dropdown is used
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Values"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Month"
                    }
                }
            }
        }
    });

    // Handle dropdown selection change
    const dataSelector = document.getElementById("dataSelector");
    dataSelector.addEventListener("change", () => {
        const selectedValue = dataSelector.value;

        // Update chart data based on the selected dropdown value
        if (selectedValue === "policyCount") {
            salesChart.data.datasets[0].data = policyCountData;
            salesChart.data.datasets[0].label = "Monthly Policy Count";
            salesChart.options.scales.y.title.text = "Policy Count";
        } else if (selectedValue === "totalPremium") {
            salesChart.data.datasets[0].data = premiumData;
            salesChart.data.datasets[0].label = "Total Premium Sales (RM)";
            salesChart.options.scales.y.title.text = "Premium (RM)";
        }

        // Update the chart to reflect the new data
        salesChart.update();
    });
});
