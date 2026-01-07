// Simple IP Check via Thordata Proxy
//
// Usage: go run simple_ip_check.go

package main

import (
	"crypto/tls"
	"encoding/json"
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
			Proxy:           http.ProxyURL(proxyURL),
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}

	targetURL := "https://httpbin.org/ip"
	fmt.Printf("🌐 Requesting: %s\n", targetURL)
	fmt.Println("   via Thordata proxy network...")

	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("❌ Error: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("❌ Error reading response: %v", err)
	}

	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		log.Fatalf("❌ Status %d: %s", resp.StatusCode, string(body))
	}

	var result map[string]interface{}
	json.Unmarshal(body, &result)

	fmt.Println("✅ Success!")
	fmt.Printf("   Your proxy IP: %s\n", result["origin"])
}
