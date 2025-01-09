document.addEventListener("DOMContentLoaded", () => {
    // Extract data from the global `vehicleData` variable
    const labels = vehicleData.map(vehicle => vehicle.Vehicle_Type);
    const data = vehicleData.map(vehicle => vehicle.NumberOfPolicies);

    // Ensure there is valid data to display
    if (labels.length === 0 || data.length === 0) {
        console.error("No data available for the chart");
        return;
    }

    // Create the chart
    const ctx = document.getElementById("vehiclesChart").getContext("2d");
    new Chart(ctx, {
        type: "pie", // Change from "bar" to "pie"
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Number of Policies",
                    data: data,
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.6)",
                        "rgba(54, 162, 235, 0.6)",
                        "rgba(255, 206, 86, 0.6)",
                        "rgba(75, 192, 192, 0.6)",
                        "rgba(153, 102, 255, 0.6)"
                    ], // Provide unique colors for each segment
                    borderColor: [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)"
                    ],
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Disable to manually control aspect ratio
            plugins: {
                legend: {
                    position: "top", // Place the legend at the top
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            const value = tooltipItem.raw;
                            return `Policies: ${value}`; // Customize tooltip label
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true, // Ensure Y-axis starts at zero
                }
            }
        }        
    });
});
