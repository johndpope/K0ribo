package K0ribo.Bittrex_Extract;

import java.sql.Timestamp;
import java.util.Iterator;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import wrapper.Bittrex;

public class Extractor {
	private String exchangeplatform;
	private String market;
	private Bittrex wrapper;
	private SQLWriter sqlWriter;
	private int interval;
	private int exchange_id;

	public Extractor(String exchangeplatform, String market, int interval, Bittrex wrapper, SQLWriter sqlWriter) {
		super();
		this.exchangeplatform = exchangeplatform;
		this.market = market;
		this.wrapper = wrapper;
		this.sqlWriter = sqlWriter;
		this.interval = interval;
		try {
			this.exchange_id = this.sqlWriter.get_exchange_id(this.exchangeplatform, this.market);
		} catch (Exception e) {
			System.err.println("Fehler beim auslesen der Exchange ID: {" + this.exchangeplatform + ", " + this.market + "}");
			this.exchange_id = -1;
		}
		new Thread(() -> this.run()).start();
	}

	public void run() {
		JsonParser parser = new JsonParser();
		while (true) {
			MarketSummary ms = new MarketSummary();
			try {
				long ts = System.currentTimeMillis();
				JsonObject requestResponse = (JsonObject) parser.parse(this.wrapper.getMarketSummary(this.market)); // Summary
				Iterator<JsonElement> summary = requestResponse.get("result").getAsJsonArray().iterator();
				while (summary.hasNext()) {
					JsonObject result = summary.next().getAsJsonObject();
					ms.setTs(new Timestamp(ts));
					ms.setTwentyfour_hour_vol(result.get("BaseVolume").getAsDouble());
					ms.setOpen_buys(result.get("OpenBuyOrders").getAsInt());
					ms.setOpen_sells(result.get("OpenSellOrders").getAsInt());
					ms.setAkt_price(result.get("Last").getAsDouble());
				}

				requestResponse = (JsonObject) parser.parse(this.wrapper.getOrderBook(this.market, Bittrex.ORDERBOOK_BOTH));
				JsonObject orderBook = requestResponse.get("result").getAsJsonObject();

				Iterator<JsonElement> buyOrders = orderBook.get("buy").getAsJsonArray().iterator();
				while (buyOrders.hasNext()) {
					JsonObject buyOrder = buyOrders.next().getAsJsonObject();
					OrderBookEntry obe = new OrderBookEntry(buyOrder.get("Rate").getAsDouble(), buyOrder.get("Quantity").getAsDouble());
					ms.getOb_buy().add(obe);
				}

				Iterator<JsonElement> sellOrders = orderBook.get("sell").getAsJsonArray().iterator();
				while (sellOrders.hasNext()) {
					JsonObject sellOrder = sellOrders.next().getAsJsonObject();
					OrderBookEntry obe = new OrderBookEntry(sellOrder.get("Rate").getAsDouble(), sellOrder.get("Quantity").getAsDouble());
					ms.getOb_buy().add(obe);
				}

				System.out.println(this.market + " Summary: " + ms);
				if (this.exchange_id > -1) {
					this.sqlWriter.writeObject(this.exchange_id, ms);
				} else {
					this.sqlWriter.writeObject(this.exchangeplatform, this.market, ms);
				}
				System.out.println("Waittime: " + (interval * 1000 - (System.currentTimeMillis() - ts)) / 1000d + " Seconds");
				Thread.sleep(interval * 1000 - (System.currentTimeMillis() - ts));

			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

}
