import { useState, useEffect, useRef, useCallback } from "react";

function useScript(src) {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    if (document.querySelector(`script[src="${src}"]`)) { setReady(true); return; }
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => setReady(true);
    document.head.appendChild(s);
  }, [src]);
  return ready;
}

const CELL = 18;

function buildMatrix(url) {
  const qr = window.QRCode.create(url, { errorCorrectionLevel: "L" });
  const sz = qr.modules.size;
  const m = [];
  for (let r = 0; r < sz; r++) {
    const row = [];
    for (let c = 0; c < sz; c++) row.push(qr.modules.get(r, c) ? 1 : 0);
    m.push(row);
  }
  return { matrix: m, size: sz };
}

export default function App() {
  const qrcodeReady = useScript("https://cdn.jsdelivr.net/npm/qrcode/build/qrcode.min.js");
  const jsqrReady   = useScript("https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js");

  const [baseUrl, setBaseUrl]       = useState("https://bit.ly/hbroldi");
  const [targetUrl, setTargetUrl]   = useState("https://bit.ly/haroldi");
  const [baseMatrix, setBaseMatrix] = useState(null);
  const [targetMatrix, setTargetMatrix] = useState(null);
  const [size, setSize]             = useState(0);
  const [diff, setDiff]             = useState(null); // list of {r,c,base,target}
  const [view, setView]             = useState("diff"); // "base" | "target" | "diff"
  const [error, setError]           = useState("");
  const canvasRef = useRef();

  const generate = useCallback(() => {
    if (!qrcodeReady || !window.QRCode) { setError("Libraries not ready, try again."); return; }
    setError("");
    try {
      const a = buildMatrix(baseUrl);
      const b = buildMatrix(targetUrl);
      if (a.size !== b.size) {
        setError(`QR codes are different sizes (${a.size}×${a.size} vs ${b.size}×${b.size}). Use shorter/longer URLs so both fit the same version.`);
        return;
      }
      const diffs = [];
      for (let r = 0; r < a.size; r++)
        for (let c = 0; c < a.size; c++)
          if (a.matrix[r][c] !== b.matrix[r][c])
            diffs.push({ r, c, base: a.matrix[r][c], target: b.matrix[r][c] });

      setBaseMatrix(a.matrix);
      setTargetMatrix(b.matrix);
      setSize(a.size);
      setDiff(diffs);
      setView("diff");
    } catch(e) {
      setError("Error: " + e.message);
    }
  }, [qrcodeReady, baseUrl, targetUrl]);

  // colour for a cell in diff view
  function cellColor(r, c) {
    const m = view === "base" ? baseMatrix : view === "target" ? targetMatrix : baseMatrix;
    const isDark = m[r][c] === 1;
    if (view === "diff" && diff) {
      const d = diff.find(d => d.r===r && d.c===c);
      if (d) {
        // base=0, target=1 → need to ADD black tile
        // base=1, target=0 → need to ADD white tile
        return d.base === 0 ? "#ff9900" : "#00aaff";
      }
    }
    return isDark ? "#111" : "#fff";
  }

  const btnStyle = (active) => ({
    padding: "7px 14px",
    fontFamily: "'DM Mono',monospace",
    fontSize: "0.73rem",
    background: active ? "#0a0a0a" : "transparent",
    color: active ? "#f5f2eb" : "#0a0a0a",
    border: "2px solid #0a0a0a",
    cursor: "pointer",
  });

  return (
    <div style={{fontFamily:"'DM Mono',monospace", background:"#f5f2eb", minHeight:"100vh", padding:"24px", userSelect:"none"}}>
      <canvas ref={canvasRef} style={{display:"none"}} />

      <div style={{fontFamily:"'Syne',sans-serif", fontSize:"2rem", fontWeight:800, letterSpacing:"-0.03em", marginBottom:4}}>
        QR Diff
      </div>
      <div style={{fontSize:"0.7rem", color:"#888", textTransform:"uppercase", letterSpacing:"0.06em", marginBottom:22}}>
        Compare two QR codes — see exactly which cells differ
      </div>

      {/* Inputs */}
      <div style={{display:"grid", gridTemplateColumns:"1fr 1fr auto", gap:8, marginBottom:20, maxWidth:780}}>
        <div>
          <div style={{fontSize:"0.62rem", textTransform:"uppercase", letterSpacing:"0.08em", color:"#888", marginBottom:5}}>Base URL (wrong)</div>
          <input value={baseUrl} onChange={e=>setBaseUrl(e.target.value)}
            style={{width:"100%", padding:"9px 11px", fontFamily:"'DM Mono',monospace", fontSize:"0.75rem",
              border:"2px solid #0a0a0a", background:"white", outline:"none"}} />
        </div>
        <div>
          <div style={{fontSize:"0.62rem", textTransform:"uppercase", letterSpacing:"0.08em", color:"#888", marginBottom:5}}>Target URL (correct)</div>
          <input value={targetUrl} onChange={e=>setTargetUrl(e.target.value)}
            style={{width:"100%", padding:"9px 11px", fontFamily:"'DM Mono',monospace", fontSize:"0.75rem",
              border:"2px solid #0a0a0a", background:"white", outline:"none"}} />
        </div>
        <div style={{display:"flex", alignItems:"flex-end"}}>
          <button onClick={generate}
            style={{padding:"9px 18px", fontFamily:"'DM Mono',monospace", fontSize:"0.78rem",
              background:"#0a0a0a", color:"#f5f2eb", border:"2px solid #0a0a0a", cursor:"pointer", whiteSpace:"nowrap"}}>
            Compare
          </button>
        </div>
      </div>

      {(!qrcodeReady || !jsqrReady) && <div style={{fontSize:"0.75rem", color:"#888", marginBottom:12}}>Loading libraries…</div>}
      {error && <div style={{color:"#e8401c", fontSize:"0.78rem", marginBottom:12}}>{error}</div>}

      {baseMatrix && diff && (
        <div style={{display:"grid", gridTemplateColumns:"auto 1fr", gap:36, alignItems:"start"}}>

          {/* Grid */}
          <div>
            {/* View toggle */}
            <div style={{display:"flex", gap:0, marginBottom:12}}>
              {[["base","Base (wrong)"],["diff","Differences"],["target","Target (correct)"]].map(([v,label])=>(
                <button key={v} onClick={()=>setView(v)} style={btnStyle(view===v)}>{label}</button>
              ))}
            </div>

            <div style={{border:"2px solid #0a0a0a", display:"inline-block", background:"white", lineHeight:0}}>
              {baseMatrix.map((row, r) => (
                <div key={r} style={{display:"flex"}}>
                  {row.map((_, c) => (
                    <div key={c} style={{
                      width: CELL, height: CELL,
                      background: cellColor(r, c),
                      outline: view==="diff" && diff.find(d=>d.r===r&&d.c===c) ? "1px solid rgba(0,0,0,0.3)" : "none",
                      boxSizing:"border-box",
                      position:"relative",
                    }}>
                      {view==="diff" && diff.find(d=>d.r===r&&d.c===c) && (
                        <div style={{
                          position:"absolute", inset:0,
                          display:"flex", alignItems:"center", justifyContent:"center",
                          fontSize: CELL*0.55+"px", lineHeight:1, color:"rgba(0,0,0,0.6)", fontWeight:"bold"
                        }}>
                          {diff.find(d=>d.r===r&&d.c===c).base===0 ? "+" : "○"}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {/* Coordinates */}
            <div style={{marginTop:10, fontSize:"0.62rem", color:"#888"}}>
              col → &nbsp;&nbsp; row ↓ &nbsp;&nbsp; (0-indexed)
            </div>
          </div>

          {/* Panel */}
          <div>
            {/* Summary */}
            <div style={{border:"2px solid #0a0a0a", padding:14, marginBottom:14, background:"white"}}>
              <div style={{fontSize:"0.6rem", textTransform:"uppercase", letterSpacing:"0.1em", color:"#888", marginBottom:10}}>Summary</div>
              <div style={{fontSize:"0.82rem", lineHeight:2}}>
                Grid size: <b>{size}×{size}</b><br/>
                Total differences: <b style={{fontSize:"1.4rem", color:"#e8401c"}}>{diff.length}</b> cells<br/>
                Add black tile: <b style={{color:"#ff9900"}}>{diff.filter(d=>d.base===0).length}</b> cells (orange)<br/>
                Add white tile: <b style={{color:"#00aaff"}}>{diff.filter(d=>d.base===1).length}</b> cells (blue)
              </div>
            </div>

            {/* Diff table */}
            <div style={{border:"2px solid #0a0a0a", background:"white", maxHeight:320, overflowY:"auto"}}>
              <div style={{padding:"10px 14px", fontSize:"0.6rem", textTransform:"uppercase", letterSpacing:"0.1em", color:"#888", borderBottom:"1px solid #ddd", position:"sticky", top:0, background:"white"}}>
                Cell coordinates (row, col)
              </div>
              {diff.map((d,i) => (
                <div key={i} style={{
                  display:"flex", alignItems:"center", gap:12,
                  padding:"7px 14px", borderBottom:"1px solid #f0f0f0",
                  fontSize:"0.75rem"
                }}>
                  <div style={{
                    width:14, height:14, flexShrink:0,
                    background: d.base===0 ? "#ff9900" : "#00aaff",
                    border:"1px solid #bbb"
                  }}/>
                  <span>Row <b>{d.r}</b>, Col <b>{d.c}</b></span>
                  <span style={{color:"#888", fontSize:"0.65rem"}}>
                    {d.base===0 ? "white→black (add black tile)" : "black→white (add white tile)"}
                  </span>
                </div>
              ))}
            </div>

            {/* Legend */}
            <div style={{marginTop:14, fontSize:"0.65rem", color:"#777"}}>
              {[
                ["#ff9900","+ = place a BLACK tile here"],
                ["#00aaff","○ = place a WHITE tile here"],
              ].map(([bg,label])=>(
                <div key={label} style={{display:"flex", alignItems:"center", gap:8, marginBottom:6}}>
                  <div style={{width:13,height:13,background:bg,border:"1px solid #bbb",flexShrink:0}}/>
                  {label}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
