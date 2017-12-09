package K0ribo.Bittrex_Extract;

import java.text.SimpleDateFormat;
import java.util.Iterator;

import org.bson.Document;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import wrapper.Bittrex;

public class Extractor {
	private String exchangeplatform;
	private String market;
	private Bittrex wrapper;
	private MongoWriter mongoWriter;
	private int interval;

	public Extractor(String exchangeplatform, String market, int interval, Bittrex wrapper, MongoWriter mongoWriter) {
		super();
		this.exchangeplatform = exchangeplatform;
		this.market = market;
		this.wrapper = wrapper;
		this.mongoWriter = mongoWriter;
		this.interval = interval;

		new Thread(() -> this.run()).start();
	}

	public void run() {
		JsonParser parser = new JsonParser();
		while (true) {
			Document d = new Document();
			JsonObject requestResponse = (JsonObject) parser.parse(this.wrapper.getMarketSummary(this.market)); // Summary
			Iterator<JsonElement> summary = requestResponse.get("result").getAsJsonArray().iterator();
			while (summary.hasNext()) {
				JsonObject result = summary.next().getAsJsonObject();
				String timeStamp = new SimpleDateFormat("yyyy.MM.dd HH.mm.ss").format(System.currentTimeMillis());
				d.append("timestamp", timeStamp);
				d.append("volume", result.get("BaseVolume").getAsDouble());
				d.append("openBuyOrders", result.get("OpenBuyOrders").getAsInt());
				d.append("openSellOrders", result.get("OpenSellOrders").getAsInt());
				d.append("price", result.get("Last").getAsDouble());
			}

			requestResponse = (JsonObject) parser
					.parse(this.wrapper.getOrderBook(this.market, Bittrex.ORDERBOOK_BOTH));
			JsonObject orderBook = requestResponse.get("result").getAsJsonObject();

			double buyVolume = 0;
			Iterator<JsonElement> buyOrders = orderBook.get("buy").getAsJsonArray().iterator();
			while (buyOrders.hasNext()) {
				JsonObject buyOrder = buyOrders.next().getAsJsonObject();
				buyVolume += buyOrder.get("Quantity").getAsDouble() * buyOrder.get("Rate").getAsDouble();
			}

			double sellVolume = 0;
			Iterator<JsonElement> sellOrders = orderBook.get("sell").getAsJsonArray().iterator();
			while (sellOrders.hasNext()) {
				JsonObject buyOrder = sellOrders.next().getAsJsonObject();
				sellVolume += buyOrder.get("Quantity").getAsDouble() * buyOrder.get("Rate").getAsDouble();
			}

			d.append("orderBookVolumeBuy", buyVolume);
			d.append("orderBookVolumeSell", sellVolume);

			buyOrders = orderBook.get("buy").getAsJsonArray().iterator();
			double buyVolumeTmp = 0;
			while (buyOrders.hasNext()) {
				JsonObject buyOrder = buyOrders.next().getAsJsonObject();
				buyVolumeTmp += buyOrder.get("Quantity").getAsDouble() * buyOrder.get("Rate").getAsDouble();
				if ((buyVolumeTmp / buyVolume) > 0.05) {
					d.append("orderBookWallBuy", buyOrder.get("Rate").getAsDouble());
					break;
				}

			}

			sellOrders = orderBook.get("sell").getAsJsonArray().iterator();
			double sellVolumeTmp = 0;
			while (sellOrders.hasNext()) {
				JsonObject sellOrder = sellOrders.next().getAsJsonObject();
				sellVolumeTmp += sellOrder.get("Quantity").getAsDouble() * sellOrder.get("Rate").getAsDouble();
				if ((sellVolumeTmp / sellVolume) > 0.05) {
					d.append("orderBookWallSell", sellOrder.get("Rate").getAsDouble());
					break;
				}

			}

			this.mongoWriter.writeDocument((this.exchangeplatform + "." + this.market), d);
			try{
				Thread.sleep(interval*1000);
			}catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

}
