document.addEventListener("DOMContentLoaded", () => {
    // Extract data from the global `salesData` variable
    const labels = salesData.map(sale => sale.Month);
    const data = salesData.map(sale => sale.Policy_Count);

    // Create the chart
    const ctx = document.getElementById("salesChart").getContext("2d");
    new Chart(ctx, {
        type: "line", // Change from "bar" to "line"
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Monthly Policy Sales",
                    data: data,
                    backgroundColor: "rgba(0, 123, 255, 0.3)", // Slightly transparent for better aesthetics
                    borderColor: "rgba(0, 123, 255, 1)", // Line color
                    borderWidth: 2, // Line thickness
                    fill: true, // Fill under the line
                    tension: 0.4 // Smooth out the line
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Disable to manually control aspect ratio
            plugins: {
                legend: {
                    position: "top",
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }        
    });
});
