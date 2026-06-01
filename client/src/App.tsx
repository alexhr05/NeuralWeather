import { useState } from "react"
import BulgariaMap from "./components/map/BulgariaMap"
import MapControlForm from "./components/map/MapControlForm"

function App() {
  const [tempValues, setTempValues] = useState<number[]>([]);

  const [currentModel, setCurrentModel] = useState<string | null>(null);

  const handleChangeTempValues = (value: number[]) => {
    setTempValues(value);
  }

  const handleModelChange = (newModel: string) => {
    setCurrentModel(newModel);
  }

  return (
    <div className="px-30 mt-10">
      <BulgariaMap
        tempValues={tempValues}
        currentModel={currentModel}
      />

      <div className="mt-5 px-3 py-4 bg-background border border-border rounded-lg">
        <MapControlForm
          onChangeTempValues={handleChangeTempValues}
          onChangeModel={handleModelChange}
        />
      </div>
    </div>
  )
}

export default App
