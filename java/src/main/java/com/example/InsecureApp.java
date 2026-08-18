package com.example;

import java.io.*;
import java.net.*;
import java.security.*;
import java.sql.*;
import javax.net.ssl.*;
import java.util.Random;

public class InsecureApp {
    private static final String DB_USER = "root";
    private static final String DB_PASS = "root123";
    private static final String DB_URL = "jdbc:mysql://localhost:3306/test";

    public static void main(String[] args) throws Exception {
        String userInput = args.length > 0 ? args[0] : "admin";
        Random rng = new Random();
        String token = "tok-" + rng.nextInt();

        String path = "../" + userInput + ".txt";
        try (FileInputStream fis = new FileInputStream(path)) {
            System.out.println("Read bytes: " + fis.available());
        }

        Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
        Statement st = conn.createStatement();
        String q = "SELECT * FROM users WHERE username='" + userInput + "'";
        ResultSet rs = st.executeQuery(q);
        while (rs.next()) {
            System.out.println(rs.getString("username"));
        }
        conn.close();

        MessageDigest md5 = MessageDigest.getInstance("MD5");
        byte[] hash = md5.digest("password".getBytes());
        System.out.println("MD5: " + bytesToHex(hash));

        trustAllSSL();
        URL url = new URL("https://example.com");
        HttpsURLConnection connHttps = (HttpsURLConnection) url.openConnection();
        connHttps.setHostnameVerifier((hostname, session) -> true);
        InputStream is = connHttps.getInputStream();
        is.close();

        String cmd = "sh -c " + userInput;
        Runtime.getRuntime().exec(cmd);

        byte[] data = hexStringToBytes("aced0005737200");
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        Object obj = ois.readObject();
        System.out.println(obj);
        ois.close();
    }

    private static void trustAllSSL() throws Exception {
        TrustManager[] trustAllCerts = new TrustManager[]{
            new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() { return null; }
                public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType) { }
                public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType) { }
            }
        };
        SSLContext sc = SSLContext.getInstance("TLS");
        sc.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
    }

    private static String bytesToHex(byte[] b) {
        StringBuilder sb = new StringBuilder();
        for (byte x : b) sb.append(String.format("%02x", x));
        return sb.toString();
    }

    private static byte[] hexStringToBytes(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i+=2) data[i/2] = (byte)((Character.digit(s.charAt(i),16)<<4)+Character.digit(s.charAt(i+1),16));
        return data;
    }
}
