import BulgariaMap from "./components/map/BulgariaMap"
import MapControlForm from "./components/map/MapControlForm"

function App() {
  return (
    <div className="px-30 mt-10">
      <BulgariaMap />

      <div className="mt-5 px-3 py-4 bg-background border border-border rounded-lg">
        <MapControlForm />
      </div>
    </div>
  )
}

export default App
