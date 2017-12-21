package K0ribo.Bittrex_Extract;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

public class MarketSummary {
	private double akt_price ;
	private Timestamp ts;
	private double twentyfour_hour_vol;
	private int open_buys;
	private int open_sells;
	private double ob_value_buy;
	private double ob_value_sell;
	private List<OrderBookEntry> ob_buy;
	private List<OrderBookEntry> ob_sell;
	
	public MarketSummary(){
		this.ob_buy = new ArrayList<OrderBookEntry>();
		this.ob_sell = new ArrayList<OrderBookEntry>();
	}
	
	public MarketSummary(Timestamp ts, double akt_price, double twentyfour_hour_vol,
			int open_buys, int open_sells, double ob_value_buy, double ob_value_sell, List<OrderBookEntry> ob_buy,
			List<OrderBookEntry> ob_sell) {
		super();
		this.akt_price = akt_price;
		this.ts = ts;
		this.twentyfour_hour_vol = twentyfour_hour_vol;
		this.open_buys = open_buys;
		this.open_sells = open_sells;
		this.ob_value_buy = ob_value_buy;
		this.ob_value_sell = ob_value_sell;
		this.ob_buy = ob_buy;
		this.ob_sell = ob_sell;
	}

	public double getAkt_price() {
		return akt_price;
	}

	public void setAkt_price(double akt_price) {
		this.akt_price = akt_price;
	}

	public Timestamp getTs() {
		return ts;
	}

	public void setTs(Timestamp ts) {
		this.ts = ts;
	}

	public double getTwentyfour_hour_vol() {
		return twentyfour_hour_vol;
	}

	public void setTwentyfour_hour_vol(double twentyfour_hour_vol) {
		this.twentyfour_hour_vol = twentyfour_hour_vol;
	}

	public int getOpen_buys() {
		return open_buys;
	}

	public void setOpen_buys(int open_buys) {
		this.open_buys = open_buys;
	}

	public int getOpen_sells() {
		return open_sells;
	}

	public void setOpen_sells(int open_sells) {
		this.open_sells = open_sells;
	}

	public double getOb_value_buy() {
		return ob_value_buy;
	}

	public void setOb_value_buy(double ob_value_buy) {
		this.ob_value_buy = ob_value_buy;
	}

	public double getOb_value_sell() {
		return ob_value_sell;
	}

	public void setOb_value_sell(double ob_value_sell) {
		this.ob_value_sell = ob_value_sell;
	}

	public List<OrderBookEntry> getOb_buy() {
		return ob_buy;
	}

	public void setOb_buy(List<OrderBookEntry> ob_buy) {
		this.ob_buy = ob_buy;
	}

	public List<OrderBookEntry> getOb_sell() {
		return ob_sell;
	}

	public void setOb_sell(List<OrderBookEntry> ob_sell) {
		this.ob_sell = ob_sell;
	}

	
	
}
