import React, {useState, useEffect} from "react";

export default function Dashboard(){
  const [logs, setLogs] = useState([]);

  // Demo: connect to a fixed task id; in prod allow selecting task and token
  useEffect(()=>{
    // no-op until user selects task — frontend includes ws client service
  },[]);

  return (
    <div style={{border:"1px solid #eee", padding:16, borderRadius:8}}>
      <h3>Realtime Progress</h3>
      <div style={{minHeight:200}}>
        {logs.length===0 ? <small>Upload a file to see progress</small> : logs.map((l,i)=> <div key={i}>{JSON.stringify(l)}</div>)}
      </div>
    </div>
  )
}
