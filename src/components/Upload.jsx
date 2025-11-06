import React, {useState} from "react";
import axios from "axios";

export default function Upload(){
  const [file, setFile] = useState(null);
  const [task, setTask] = useState(null);

  async function submit(){
    const fd = new FormData();
    fd.append("file", file);
    const res = await axios.post("/upload", fd, {headers: {"Authorization": "Bearer REPLACE_TOKEN"}});
    setTask(res.data.task_id);
  }

  return (
    <div style={{border:"1px solid #eee", padding:16, borderRadius:8}}>
      <h3>Upload docx / pdf</h3>
      <input type="file" onChange={(e)=>setFile(e.target.files[0])}/>
      <button onClick={submit} disabled={!file} style={{marginLeft:10}}>Upload</button>
      {task && <div>Task: {task}</div>}
    </div>
  )
}
