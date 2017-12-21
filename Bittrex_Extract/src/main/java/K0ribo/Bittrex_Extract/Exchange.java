package K0ribo.Bittrex_Extract;

import java.util.ArrayList;
import java.util.List;

public class Exchange {
	private String platform;
	private List<String> markets;
	
	public Exchange(){
		this.markets = new ArrayList<String>();
	}
	public Exchange(String platform, List<String> markets) {
		super();
		this.platform = platform;
		this.markets = markets;
	}
	public String getPlatform() {
		return platform;
	}
	public void setPlatform(String platform) {
		this.platform = platform;
	}
	public List<String> getMarkets() {
		return markets;
	}
	public void setMarkets(List<String> markets) {
		this.markets = markets;
	}
	
	
}
