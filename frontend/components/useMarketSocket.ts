useEffect(() => {
  const ws = new WebSocket("ws://127.0.0.1:8000/ws/market");

  ws.onopen = () => console.log("✅ WS connected");

  ws.onmessage = (e) => {
    console.log("📩", e.data);
  };

  ws.onerror = (e) => console.log("❌ WS error", e);

  ws.onclose = () => console.log("🔌 WS closed");

  return () => ws.close();
}, []);
