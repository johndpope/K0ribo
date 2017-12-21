package K0ribo.Bittrex_Extract;

public class OrderBookEntry {
	private double price;
	private double amount;
	
	public OrderBookEntry(double price, double amount) {
		super();
		this.price = price;
		this.amount = amount;
	}

	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public double getAmount() {
		return amount;
	}

	public void setAmount(double amount) {
		this.amount = amount;
	}
	
}
