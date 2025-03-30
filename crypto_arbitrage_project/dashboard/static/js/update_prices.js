function updatePrices() {
    $.ajax({
      url: "/get_prices", // Ensure this URL matches your Django URL configuration
      method: "GET",
      success: function(data) {
        // Update the real-time prices table
        let priceTableBody = $("#price-table-body");
        priceTableBody.empty();
        data.prices.forEach(function(item) {
          let row = `<tr>
            <td>${item.pair}</td>`;
          let exchanges = ["Binance", "Kraken", "Coinbase", "Bitfinex"];
          exchanges.forEach(function(ex) {
            let priceData = item.prices[ex];
            let ask = priceData && priceData.ask ? priceData.ask : "N/A";
            let bid = priceData && priceData.bid ? priceData.bid : "N/A";
            row += `<td>${ask}</td><td>${bid}</td>`;
          });
          row += `</tr>`;
          priceTableBody.append(row);
        });
  
        // Update the arbitrage opportunities table
        let arbTableBody = $("#arbitrage-table-body");
        arbTableBody.empty();
        data.arbitrage_opportunities.forEach(function(opp) {
          let row = `<tr>
            <td>${opp.pair}</td>
            <td>${opp.buy_exchange}</td>
            <td>${opp.buy_price}</td>
            <td>${opp.sell_exchange}</td>
            <td>${opp.sell_price}</td>
            <td>${opp.profit_pct}</td>
          </tr>`;
          arbTableBody.append(row);
        });
      },
      error: function(err) {
        console.error("Error fetching prices:", err);
      }
    });
  }
  
  // Initial call and set interval to update every 10 seconds
  $(document).ready(function() {
    updatePrices();
    setInterval(updatePrices, 1000);
  });
  