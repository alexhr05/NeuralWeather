import { useState } from "react"
import BulgariaMap from "./components/map/BulgariaMap"
import MapControlForm from "./components/map/MapControlForm"

function App() {
  const [tempValues, setTempValues] = useState<number[]>([]);

  const handleChangeTempValues = (value: number[]) => {
    setTempValues(value);
  }

  return (
    <div className="px-30 mt-10">
      <BulgariaMap tempValues={tempValues} />

      <div className="mt-5 px-3 py-4 bg-background border border-border rounded-lg">
        <MapControlForm onChangeTempValues={handleChangeTempValues} />
      </div>
    </div>
  )
}

export default App
