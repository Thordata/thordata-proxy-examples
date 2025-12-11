// Simple IP Check via Thordata Proxy
//
// Usage: go run simple_ip_check.go

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
)

func main() {
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

	// Build proxy URL
	proxyUsername := fmt.Sprintf("td-customer-%s", username)
	proxyURL := &url.URL{
		Scheme: "http",
		User:   url.UserPassword(proxyUsername, password),
		Host:   fmt.Sprintf("%s:%s", host, port),
	}

	// Create HTTP client with proxy
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxyURL),
		},
	}

	targetURL := "https://httpbin.org/ip"
	fmt.Printf("🌐 Requesting: %s\n", targetURL)
	fmt.Println("   via Thordata proxy network...")
	fmt.Println()

	resp, err := client.Get(targetURL)
	if err != nil {
		log.Fatalf("❌ Error: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("❌ Error reading response: %v", err)
	}

	var result map[string]interface{}
	json.Unmarshal(body, &result)

	fmt.Println("✅ Success!")
	fmt.Printf("   Your proxy IP: %s\n", result["origin"])
}