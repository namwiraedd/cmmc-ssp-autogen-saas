import React from "react";
import Upload from "./components/Upload";
import Dashboard from "./components/Dashboard";

export default function App(){
  return (
    <div style={{padding:20,fontFamily:"Inter, system-ui"}}>
      <h1>SSP Generator Dashboard</h1>
      <div style={{display:"flex", gap:20}}>
        <div style={{flex:1}}><Upload/></div>
        <div style={{flex:1}}><Dashboard/></div>
      </div>
    </div>
  )
}
