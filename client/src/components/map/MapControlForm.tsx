import { useState, useEffect, useMemo } from "react";
import { useForm } from "react-hook-form";
import * as Yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import FormProvider from "../form/FormProvider";
// import { RHFTextField } from '../form/RHFTextField';
import { RHFDropdown } from "../form/RHFDropdown";
import { Button } from "../common/Button";
import { getTemperatures } from "../../services/temperatureService";
import { getBulgariaCoordinates } from "../../utils/bulgariaCoordinates";
import { getModels } from "../../services/modelService";

type Props = {
  latitude?: number;
  longitude?: number;
  onChangeTempValues: (value: number[]) => void;
  onChangeModel: (newModel: string) => void;
};

type FormValues = {
  hour: string;
  day: string;
  month: string;
  year: string;
  latitude: number;
  longitude: number;
  model: string;
};

const schema = Yup.object({
  hour: Yup.string().required("Hour is required"),
  day: Yup.string().required("Day is required"),
  month: Yup.string().required("Month is required"),
  year: Yup.string().required("Year is required"),
  latitude: Yup.number().required("Latitude is required"),
  longitude: Yup.number().required("Longitude is required"),
  model: Yup.string().required("Model is required"),
});

export default function MapControlForm({
  latitude,
  longitude,
  onChangeTempValues,
  onChangeModel,
}: Props) {
  const [modelOptions, setModelOptions] = useState<string[]>([]);

  useEffect(() => {
    const fetchModels = async () => {
      const res = await getModels();
      setModelOptions(res);
    };

    fetchModels();
  }, []);

  const defaultValues = useMemo(
    () => ({
      hour: "",
      day: "",
      month: "",
      year: "",
      latitude: latitude ?? 0,
      longitude: longitude ?? 0,
      model: "",
    }),
    [latitude, longitude],
  );

  const methods = useForm<FormValues>({
    defaultValues,
    resolver: yupResolver(schema),
  });

  const { handleSubmit } = methods;

  const onSubmit = handleSubmit(async (data) => {
    const reqBody = {
      year: Number(data.year),
      month: Number(data.month),
      day: Number(data.day),
      hour: Number(data.hour),
      coordinate: getBulgariaCoordinates(),
      model: data.model,
    };

    try {
      const res = await getTemperatures(reqBody);
      onChangeTempValues(res);
      onChangeModel(data.model);
    } catch (error) {
      console.error(error);
    }
  });

  const hourOptions = Array.from({ length: 24 }, (_, i) => ({
    value: String(i),
    label: `${i}:00`,
  }));

  const dayOptions = Array.from({ length: 31 }, (_, i) => ({
    value: String(i + 1),
    label: String(i + 1),
  }));

  const monthOptions = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ].map((name, i) => ({
    value: String(i + 1),
    label: name,
  }));

  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from({ length: currentYear - 1979 }, (_, i) => ({
    value: String(currentYear - i),
    label: String(currentYear - i),
  }));

  return (
    <FormProvider
      methods={methods}
      onSubmit={onSubmit}
      className="flex flex-1 gap-2 w-full"
    >
      <RHFDropdown fullWidth name="hour" label="Hour" options={hourOptions} />
      <RHFDropdown fullWidth name="day" label="Day" options={dayOptions} />
      <RHFDropdown
        fullWidth
        name="month"
        label="Month"
        options={monthOptions}
      />
      <RHFDropdown fullWidth name="year" label="Year" options={yearOptions} />
      {/* <RHFTextField name='latitude' label='Latitude' fullWidth />
      <RHFTextField name='longitude' label='Longitude' fullWidth /> */}
      <RHFDropdown
        fullWidth
        name="model"
        label="Model"
        options={modelOptions}
      />

      <Button
        type="submit"
        variant="glass"
        className="self-end shrink-0 border border-transparent"
      >
        Submit
      </Button>
    </FormProvider>
  );
}
