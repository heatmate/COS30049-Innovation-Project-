import React, { useState } from "react"
import PieData from "./PieData"
import HeatmapData from "./HeatmapData";
import "./App.css"

function App() {
  const [file, setFile] = useState(null)
  const [errorMsg, setErrorMsg] = useState("")
  const [visualizations, showVisulisations] = useState(false)
  const validFileTypes = ['.py', '.html', '.php']

  const fileChanged = (e) => {
    const selectedFiles = e.target.files
    let selectedFile = null
    let selectedFileType = null

    /* VALIDATES EXISTANCE */
    if (!selectedFiles || selectedFiles.length === 0) {
      invalid("Please Upload a File")
      return
    }

    /* VALIDATES SINGLE FILE UPLOAD */
    if (selectedFiles.length > 1){
      invalid("Too Many Files Uploaded")
      return
    } else {
      selectedFile = selectedFiles[0]
    }

    /* VALIDATES FILE TYPE */
    if (selectedFile){
      selectedFileType = selectedFile.name.split('.').pop()
      if(!validFileTypes.includes('.' + selectedFileType.toLowerCase())) {
        invalid("Invalid File is Type: ." + selectedFileType)
        return
      }

      /* VALIDATES FILE SIZE*/
      if (selectedFile.size <= 0) {
        invalid("Selected File is Empty")
        return
      }
      else if(selectedFile.size > 5 * 1024 * 1024){
        invalid("File Size Too Large: " + (selectedFile.size / 1024 / 1024).toFixed(2)  + " megabytes")
        return
      }
    }
  
    setFile(selectedFile)
    setErrorMsg("")
    showVisulisations(true)
  }

  const invalid = (message) => {
      setErrorMsg("⚠ " + message)
      setFile(null)
      return
  }

  return (
    <div className="main">
      <form>
        <label>Please Upload a File</label>
        <table style={{width: "100%"}}>
          <tr>
            <td>
              <input type="file" required onChange={fileChanged} className="uploadFile"></input>
            </td>
          </tr>
          <tr>
            <td>
              {errorMsg && <p aria-live="polite" style={{ color: 'red' }}>{errorMsg}</p>}
              {file && <p>Selected File: {file.name}</p>}
            </td>
          </tr>
          <tr>
            <td>
              <button type="submit" disabled={!file} className="uploadButton">Analyse</button>    
            </td>
          </tr>
        </table>
      </form>

      {visualizations && (
        <div className="graphs">
        <div className="flex justify-center items-center h-screen bg-gray-50">
          <PieData />
        </div>
        <div className="p-8">
          <HeatmapData />
        </div>
      </div>
      )}
      
    </div>
  )
}
export default App