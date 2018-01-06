package K0ribo.Bittrex_Extract;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

public class SQLWriter {

	private String CREATE_TABLE_EXCHANGE = "CREATE TABLE IF NOT EXISTS exchanges ( id INTEGER PRIMARY KEY, "
			+ "exchange char(50), market char(15), UNIQUE(exchange, market))";
	private String CREATE_TABLE_MARKET_SUMMARY = "CREATE TABLE IF NOT EXISTS market_summary ( exchange_id INTEGER, ts timestamp, "
			+ "akt_preis double, twentyfour_hour_vol double, open_buys INTEGER, open_sells INTEGER, ob_value_buy double, ob_value_sell double,"
			+ "FOREIGN KEY(exchange_id) REFERENCES exchanges(id), PRIMARY KEY (exchange_id, ts))";
	private String CREATE_TABLE_ORDERBOOK = "CREATE TABLE IF NOT EXISTS orderbook (exchange_id INTEGER, ts timestamp, price double, amount double, type INTEGER)";
	private String GET_EXCHANGE = "SELECT * FROM exchanges WHERE exchange = ? AND market = ?";
	private String INSERT_EXCHANGE = "INSERT INTO exchanges (exchange, market) VALUES(?,?)";
	private String INSERT_MARKET_SUMMARY = "INSERT INTO market_summary VALUES (?,?,?,?,?,?,?,?)";
	private String INSERT_INTO_ORDERBOOK = "INSERT INTO orderbook VALUES (?,?,?,?,?)";

	private Connection c;

	public SQLWriter(String url, String db, List<Exchange> exchanges) {
		super();
		try {
			Class.forName("org.sqlite.JDBC");
			c = DriverManager.getConnection("jdbc:sqlite:" + url + "." + db);
		} catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());
			System.exit(0);
		}
		System.out.println("Opened database successfully");
		this.initialize(exchanges);
	}

	public void initialize(List<Exchange> exchanges) {
		try {
			Statement stmt;
			stmt = this.c.createStatement();
			stmt.executeUpdate(this.CREATE_TABLE_EXCHANGE);
			stmt = this.c.createStatement();
			stmt.executeUpdate(this.CREATE_TABLE_MARKET_SUMMARY);
			stmt = this.c.createStatement();
			stmt.executeUpdate(this.CREATE_TABLE_ORDERBOOK);

			for (Exchange e : exchanges) {
				for (String market : e.getMarkets()) {
					try {
						PreparedStatement pstmt = this.c.prepareStatement(this.INSERT_EXCHANGE);
						pstmt.setString(1, e.getPlatform());
						pstmt.setString(2, market);
						pstmt.executeUpdate();
					} catch (Exception e2) {
						System.out.println("Element: " + e.toString() + " existiert bereits");
					}
				}
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void writeObject(String exchange, String market, MarketSummary summary) {
		try {
			int exchange_id = this.get_exchange_id(exchange, market);
			this.writeObject(exchange_id, summary);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void writeObject(int exchange_id, MarketSummary summary) {
		PreparedStatement stmt;
		try {
			stmt = this.c.prepareStatement(this.INSERT_MARKET_SUMMARY);
			stmt.setInt(1, exchange_id);
			stmt.setTimestamp(2, summary.getTs());
			stmt.setDouble(3, summary.getAkt_price());
			stmt.setDouble(4, summary.getTwentyfour_hour_vol());
			stmt.setInt(5, summary.getOpen_buys());
			stmt.setInt(6, summary.getOpen_sells());
			stmt.setDouble(7, summary.getOb_value_buy());
			stmt.setDouble(8, summary.getOb_value_sell());
			stmt.executeUpdate();
			Statement simpleStmt = this.c.createStatement();
			simpleStmt.execute("BEGIN TRANSACTION;");
			for (OrderBookEntry obe : summary.getOb_buy()) {
				stmt = this.c.prepareStatement(this.INSERT_INTO_ORDERBOOK);
				stmt.setInt(1, exchange_id);
				stmt.setTimestamp(2, summary.getTs());
				stmt.setDouble(3, obe.getPrice());
				stmt.setDouble(4, obe.getAmount());
				stmt.setInt(5, 1);
				stmt.executeUpdate();
			}
			for (OrderBookEntry obe : summary.getOb_sell()) {
				stmt = this.c.prepareStatement(this.INSERT_INTO_ORDERBOOK);
				stmt.setInt(1, exchange_id);
				stmt.setTimestamp(2, summary.getTs());
				stmt.setDouble(3, obe.getPrice());
				stmt.setDouble(4, obe.getAmount());
				stmt.setInt(5, 2);
				stmt.executeUpdate();
			}
			simpleStmt = this.c.createStatement();
			simpleStmt.execute("COMMIT;");
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public int get_exchange_id(String exchange, String market) throws Exception {
		try {
			PreparedStatement stmt = this.c.prepareStatement(this.GET_EXCHANGE);
			stmt.setString(1, exchange);
			stmt.setString(2, market);
			ResultSet rs = stmt.executeQuery();
			while (rs.next()) {				
				return rs.getInt(1);
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		throw new Exception("Exchange Not Found!");

	}

	public boolean insert_exchange(String platform, String market) {
		try {
			PreparedStatement stmt = this.c.prepareStatement(this.INSERT_EXCHANGE);
			stmt.setString(1, platform);
			stmt.setString(2, market);
			return stmt.execute();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
	}

}
