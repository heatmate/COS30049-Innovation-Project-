import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import FileUploader from './components/FileUpload'

function App() {
  return (
    <>
      <div>
        <h1>Software Vulnerability Detection</h1>
        <FileUploader />
      </div>
    </>
  )
}

export default App
