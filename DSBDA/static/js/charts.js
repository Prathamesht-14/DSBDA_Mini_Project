document.addEventListener("DOMContentLoaded", function() {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: { family: "'Inter', sans-serif" }
                }
            }
        },
        animation: {
            duration: 1500,
            easing: 'easeOutQuart'
        }
    };

    // Only fetch if we're on a page with charts (dashboard or analysis)
    if(document.getElementById('monthlyTrendChart') || document.getElementById('analysisMonthlyTrend')) {
        fetch('/api/chart-data')
            .then(res => res.json())
            .then(data => {
                if(data.error) return;

                // Dashboard Charts
                if(document.getElementById('monthlyTrendChart')) {
                    new Chart(document.getElementById('monthlyTrendChart').getContext('2d'), {
                        type: 'line',
                        data: {
                            labels: data.monthly_trend.labels,
                            datasets: [{
                                label: 'Monthly Sales ($)',
                                data: data.monthly_trend.values,
                                borderColor: '#0d47a1',
                                backgroundColor: 'rgba(13, 71, 161, 0.1)',
                                borderWidth: 2,
                                fill: true,
                                tension: 0.4
                            }]
                        },
                        options: commonOptions
                    });

                    new Chart(document.getElementById('categorySalesChart').getContext('2d'), {
                        type: 'doughnut',
                        data: {
                            labels: data.category_sales.labels,
                            datasets: [{
                                data: data.category_sales.values,
                                backgroundColor: ['#0d47a1', '#00d2ff', '#1a237e', '#82b1ff'],
                                borderWidth: 0
                            }]
                        },
                        options: { ...commonOptions, plugins: { legend: { position: 'right' } } }
                    });

                    new Chart(document.getElementById('regionSalesChart').getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: data.region_sales.labels,
                            datasets: [{
                                label: 'Sales by Region',
                                data: data.region_sales.values,
                                backgroundColor: '#00d2ff',
                                borderRadius: 5
                            }]
                        },
                        options: { ...commonOptions, scales: { y: { beginAtZero: true } } }
                    });

                    new Chart(document.getElementById('segmentProfitChart').getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: data.segment_profit.labels,
                            datasets: [{
                                label: 'Profit by Segment',
                                data: data.segment_profit.values,
                                backgroundColor: '#1a237e',
                                borderRadius: 5
                            }]
                        },
                        options: { ...commonOptions, scales: { y: { beginAtZero: true } } }
                    });
                }

                // Analysis Charts
                if(document.getElementById('analysisMonthlyTrend')) {
                    new Chart(document.getElementById('analysisMonthlyTrend').getContext('2d'), {
                        type: 'line',
                        data: {
                            labels: data.monthly_trend.labels,
                            datasets: [{
                                label: 'Sales Trend',
                                data: data.monthly_trend.values,
                                borderColor: '#00d2ff',
                                backgroundColor: 'rgba(0, 210, 255, 0.2)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4,
                                pointRadius: 4,
                                pointHoverRadius: 6
                            }]
                        },
                        options: commonOptions
                    });

                    new Chart(document.getElementById('analysisRegionChart').getContext('2d'), {
                        type: 'pie',
                        data: {
                            labels: data.region_sales.labels,
                            datasets: [{
                                data: data.region_sales.values,
                                backgroundColor: ['#0d47a1', '#00d2ff', '#1a237e', '#82b1ff'],
                                borderWidth: 2,
                                borderColor: '#ffffff'
                            }]
                        },
                        options: commonOptions
                    });

                    new Chart(document.getElementById('analysisCategoryChart').getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: data.category_sales.labels,
                            datasets: [{
                                label: 'Revenue',
                                data: data.category_sales.values,
                                backgroundColor: '#1a237e',
                                borderRadius: 8
                            }]
                        },
                        options: { ...commonOptions, scales: { y: { beginAtZero: true } } }
                    });
                }
            })
            .catch(err => console.error("Error loading chart data:", err));
    }
});
