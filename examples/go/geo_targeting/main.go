// Geo-Targeted Request via Thordata Proxy
//
// Usage:
//   go run geo_targeting/main.go
//   go run geo_targeting/main.go -country de

package main

import (
	"crypto/tls"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"

	"github.com/joho/godotenv"
)

func loadEnv() {

	_ = godotenv.Load("../../.env")
}

func main() {
	loadEnv()

	country := flag.String("country", "us", "Target country code")
	flag.Parse()

	username := os.Getenv("THORDATA_USERNAME")
	password := os.Getenv("THORDATA_PASSWORD")
	host := os.Getenv("THORDATA_PROXY_HOST")
	port := os.Getenv("THORDATA_PROXY_PORT")

	if host == "" {
		host = "pr.thordata.net"
	}
	if port == "" {
		port = "9999"
	}

	if username == "" || password == "" {
		log.Fatal("❌ Error: Set THORDATA_USERNAME and THORDATA_PASSWORD in .env")
	}

	// Build username with geo-targeting
	proxyUsername := fmt.Sprintf("td-customer-%s-country-%s", username, *country)

	// Scheme MUST be http for port 9999 usually
	proxyURL := &url.URL{
		Scheme: "http",
		User:   url.UserPassword(proxyUsername, password),
		Host:   fmt.Sprintf("%s:%s", host, port),
	}

	fmt.Printf("🌍 Geo-targeting: %s\n", *country)
	fmt.Printf("   Username: %s\n\n", proxyUsername)

	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxyURL),
			// Ignore SSL errors (common in proxy chains)
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}

	targetURL := "https://ipinfo.io/json"
	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		log.Fatal(err)
	}
	// Add User-Agent to avoid being blocked by target
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("❌ Error: %v", err)
	}
	defer resp.Body.Close() //nolint:errcheck

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("❌ Error reading body: %v", err)
	}

	if resp.StatusCode != 200 {
		log.Fatalf("❌ API Error (Status %d): %s", resp.StatusCode, string(body))
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		log.Fatalf("❌ JSON Parse Error: %v\nBody: %s", err, string(body))
	}

	fmt.Println("✅ Response:")
	fmt.Printf("   IP:      %v\n", result["ip"])
	fmt.Printf("   Country: %v\n", result["country"])
	fmt.Printf("   Region:  %v\n", result["region"])
	fmt.Printf("   City:    %v\n", result["city"])
}
