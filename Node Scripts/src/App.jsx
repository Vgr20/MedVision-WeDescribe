import { useEffect, useState } from 'react'

function App() {
  const [RBC,setRBC] = useState();
  const [Hemoglobin, setHemoglobin] = useState();
  const [Lymphocytes,setLymphocytes] = useState();
  const [PackCellVolume, setPackCellVolume] = useState();
  const [MeanPlateletVolume, setMeanPlateletVolume] = useState();
  const [MeanCellVolume, setMeanCellVolume] = useState();
  const [Platelet , setPlatelet] = useState();
  const [MeanCellHaemoglobin, setMeanCellHaemoglobin] = useState();
  const [TotalWhiteCellCount, setTotalWhiteCellCount] = useState();
  const [MeancellhaemoglobinConcentration, setMeancellhaemoglobinConcentration] = useState();
  const [RedCellDistribution, setRedCellDistribution] = useState();
  const [Neutrophils, setNeutrophils] = useState();
  const [Eosinophils, setEosinophils] = useState();
  const [Monocytes, setMonocytes] = useState();
  const [Basophils, setBasophils] = useState();
  const [Thought, setThought] = useState();
  const [Text,setText] = useState();

  useEffect(() => {
    const fetchTextFile = async () => {
      try {
        const response = await fetch('src/assets/prompt.json');
        const jsonData = await response.json();

        const response_2 = await fetch('src/assets/prompt_2.json');
        const jsonData_2 = await response_2.json();

        const response_3 = await fetch('src/assets/prompt_3.json');
        const jsonData_3 = await response_3.json();

        const lymphocytes = jsonData['LYMPHOCYTES'];
        setLymphocytes(lymphocytes);

        const hemoglobin = jsonData['HAEMOGLOBIN'];
        setHemoglobin(hemoglobin);

        const rbc = jsonData['RED BLOOD CELLS'];
        setRBC(rbc);

        const packCellVolume = jsonData['PACK CELL VOLUME'];
        setPackCellVolume(packCellVolume);

        const meanPlateletVolume = jsonData['MPV'];
        setMeanPlateletVolume(meanPlateletVolume);

        const meanCellVolume = jsonData['MEAN CELL VOLUME'];
        setMeanCellVolume(meanCellVolume);

        const platelet = jsonData['PLATELET COUNT'];
        setPlatelet(platelet);

        const meanCellHaemoglobin = jsonData['MEAN CELL HAEMOGLOBIN'];
        setMeanCellHaemoglobin(meanCellHaemoglobin);

        const totalWhiteCellCount = jsonData['TOTAL WHITE CELL COUNT'];
        setTotalWhiteCellCount(totalWhiteCellCount);

        const meanCellHaemoglobinConcentration = jsonData['MEAN CELL HEAMOGLOBIN CONCENTRATION'];
        setMeancellhaemoglobinConcentration(meanCellHaemoglobinConcentration);

        const redCellDistribution = jsonData['RED CELL DISTRIBUTION WIDTH'];
        setRedCellDistribution(redCellDistribution);

        const neutrophils = jsonData['NEUTROPHILS'];
        setNeutrophils(neutrophils);

        const eosinophils = jsonData['EOSINOPHILS'];
        setEosinophils(eosinophils);

        const monocytes = jsonData['MONOCYTES'];
        setMonocytes(monocytes);

        const basophils = jsonData['BASOPHILS'];
        setBasophils(basophils);

        const thought = jsonData_2['bubbld_msg'];
        setThought(thought);

        const text = jsonData_3['TEXT'];
        setText(text);

      } catch (error) {
        console.error('Error Fetching text file: ',error);
      }
    };
    fetchTextFile();
  }, []);

  const myname = "This is my name"

  return (
  <div className="flex justify-start items-stretch ps-20 pt-20 w-screen h-screen">
      <div className="grid grid-cols-7 gap-x-24 justify-items-stretch">
        <div className="relative -translate-y-2 col-span-1">
          <img
            src="src/assets/RED BLOOD CELLS_gauge.png"
            alt="Red Blood Cells"
            className="w-auto h-28 rounded-lg shadow-lg"
          />
          <div className="absolute -translate-y-6 -translate-x-20 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-opacity duration-1000">
            <p className="text-white text-center">{RBC}</p>
          </div>
        </div>
        <div className="relative -translate-y-2 translate-x-8 col-span-3">
          <img
            src="src/assets/HAEMOGLOBIN_gauge.png"
            alt="Hemoglobin"
            className="w-auto h-28 rounded-lg shadow-lg"
          />
          <div className="absolute -translate-y-6 w-96 inset-0 flex z-20 justify-center items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-opacity duration-1000">
            <p className="text-white text-center">{Hemoglobin}</p>
          </div>
        </div>
        <div className="relative translate-y-28 translate-x-12 col-span-2">
          <img
            src="src/assets/MPV_gauge.png"
            alt="Mean Platelett Volume"
            className="w-auto h-28 rounded-lg shadow-lg"
          />
          <div className="absolute -translate-y-6 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-x-44 duration-1000">
            <p className="text-white text-center">{MeanPlateletVolume}</p>
          </div>
        </div>
        <div className="relative translate-y-28 -translate-x-56 col-span-1">
          <div className="absolute w-96 h-auto inset-0 flex z-20 justify-stretch items-stretch bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-y-20 duration-1000">
            <p className="text-black text-center">Contact Doctor</p>
          </div>
        </div>
        <div className="relative translate-y-6 col-span-4">
          <img
            src="src/assets/PACK CELL VOLUME_gauge.png"
            alt="Pack cell Volume"
            className="w-auto h-28 rounded-3xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-x-44 duration-1000">
            <p className="text-white text-center">{PackCellVolume}</p>
          </div>
        </div>
        <div className="relative translate-y-32 translate-x-12 col-span-2">
          <img
            src="src/assets/PLATELET COUNT_gauge.png"
            alt="Platelet Count"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-x-44 duration-1000">
            <p className="text-white text-center">{Platelet}</p>
          </div>
        </div>
        <div className="relative translate-y-12 col-span-2">
          <img
            src="src/assets/MEAN CELL VOLUME_gauge.png"
            alt="Mean Cell Volume"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 h-32 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-x-44 duration-1000">
            <p className="text-white text-center">{MeanCellVolume}</p>
          </div>
        </div>
        <div className="relative translate-x-28 translate-y-16 col-span-4">
          <img
            src="src/assets/fbc_1_table_0_overall_expression.png"
            alt="Smiliey Blood"
            className="w-auto h-56 rounded-full shadow-lg "
          />
          <div className="absolute pb-6 -translate-x-40 w-44 inset-0 flex z-20 justify-center items-center bg-opacity-70 rounded-full opacity-100 hover:scale-110 transition -translate-y-64 duration-1000">
            <p className="text-black text-center">{Thought}</p>
          </div>
        </div>
        <div className="relative -translate-y-10 col-span-6">
          <img
            src="src/assets/MEAN CELL HAEMOGLOBIN_gauge.png"
            alt="Mean Cell Haemoglobin"
            className="w-auto h-28 rounded-lg shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:translate-x-44 duration-1000">
            <p className="text-white text-center">{MeanCellHaemoglobin}</p>
          </div>
        </div>
        <div className="relative -translate-y-16 col-span-1">
          <img
            src="src/assets/TOTAL WHITE CELL COUNT_gauge.png"
            alt="Total White Cell Count"
            className="w-auto h-28 rounded-lg shadow-lg "
          />
          <div className="absolute -translate-x-52 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{TotalWhiteCellCount}</p>
          </div>
        </div>
        <div className="relative translate-y-2 row-start-5 col-span-1">
          <img
            src="src/assets/MEAN CELL HEAMOGLOBIN CONCENTRATION_gauge.png"
            alt="Mean Cell Hemoglobin Concentration"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 -translate-x-20 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-opacity duration-1000">
            <p className="text-white text-center">{MeancellhaemoglobinConcentration}</p>
          </div>
        </div>
        <div className="relative translate-y-2 translate-x-10 row-start-5 col-span-1">
          <img
            src="src/assets/RED CELLDISTRIBUTION WIDTH_gauge.png"
            alt="Red Cell Distribution Width"
            className="w-auto h-28 rounded-3xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 -translate-x-20 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{RedCellDistribution}</p>
          </div>
        </div>
        <div className="relative translate-y-2 translate-x-20 row-start-5 col-span-1">
          <img
            src="src/assets/NEUTROPHILS_gauge.png"
            alt="Neutrophils"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 -translate-x-20 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000 ease-out">
            <p className="text-white text-center">{Neutrophils}</p>
          </div>
        </div>
        <div className="relative translate-y-2 translate-x-20 row-start-5 col-span-1">
          <img
            src="src/assets/LYMPHOCYTES_gauge.png"
            alt="Lymphocytes"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 -translate-x-20 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{Lymphocytes}</p>
          </div>
        </div>
        <div className="relative translate-y-2 translate-x-16 row-start-5 col-span-1">
          <img
            src="src/assets/EOSINOPHILS_gauge.png"
            alt="Eosinophils"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 -translate-x-20 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{Eosinophils}</p>
          </div>
        </div>
        <div className="relative  translate-x-8 row-start-5 col-span-1">
          <img
            src="src/assets/MONOCYTES_gauge.png"
            alt="Monocytes"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 w-96 -translate-x-20 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{Monocytes}</p>
          </div>
        </div>
        <div className="relative row-start-5 col-span-1">
          <img
            src="src/assets/BASOPHILS_gauge.png"
            alt="Basophils"
            className="w-auto h-28 rounded-2xl shadow-lg "
          />
          <div className="absolute -translate-y-6 -translate-x-52 w-96 inset-0 flex z-20 justify-end items-center bg-black bg-opacity-70 rounded-lg opacity-0 hover:opacity-100 transition-transform hover:-translate-y-44 duration-1000">
            <p className="text-white text-center">{Basophils}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
