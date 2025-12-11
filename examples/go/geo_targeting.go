// Geo-Targeted Request via Thordata Proxy
//
// Usage:
//   go run geo_targeting.go
//   go run geo_targeting.go -country de

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
)

func main() {
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
		log.Fatal("❌ Error: Set THORDATA_USERNAME and THORDATA_PASSWORD")
	}

	// Build username with geo-targeting
	proxyUsername := fmt.Sprintf("td-customer-%s-country-%s", username, *country)
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
		},
	}

	resp, err := client.Get("https://ipinfo.io/json")
	if err != nil {
		log.Fatalf("❌ Error: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("❌ Error: %v", err)
	}

	var result map[string]interface{}
	json.Unmarshal(body, &result)

	fmt.Println("✅ Response:")
	fmt.Printf("   IP:      %s\n", result["ip"])
	fmt.Printf("   Country: %s\n", result["country"])
	fmt.Printf("   Region:  %s\n", result["region"])
	fmt.Printf("   City:    %s\n", result["city"])
}