import { useMemo } from 'react';
import { useForm } from 'react-hook-form'
import * as Yup from "yup"
import { yupResolver } from '@hookform/resolvers/yup'
import FormProvider from '../form/FormProvider';
import { RHFTextField } from '../form/RHFTextField';
import { RHFDropdown } from '../form/RHFDropdown';
import { Button } from '../common/Button';

type Props = {
  latitude?: number;
  longitude?: number;
}

type FormValues = {
  day: string;
  month: string;
  year: string;
  latitude: number;
  longitude: number;
  model: string
};

const schema = Yup.object({
  day: Yup.string().required('Day is required'),
  month: Yup.string().required('Month is required'),
  year: Yup.string().required('Year is required'),
  latitude: Yup.number().required('Latitude is required'),
  longitude: Yup.number().required('Longitude is required'),
  model: Yup.string().required('Model is required')
});

export default function MapControlForm({ latitude, longitude }: Props) {

  const defaultValues = useMemo(
    () => ({
      day: '',
      month: '',
      year: '',
      latitude: latitude ?? 0,
      longitude: longitude ?? 0,
      model: ''
    }),
    [latitude, longitude]
  );

  const methods = useForm<FormValues>({
    defaultValues,
    resolver: yupResolver(schema),
  });

  const { handleSubmit } = methods;

  const onSubmit = handleSubmit((data) => {
    console.log(data);
  });

  const dayOptions = Array.from({ length: 31 }, (_, i) => ({
    value: String(i + 1),
    label: String(i + 1),
  }));

  const monthOptions = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ].map((name, i) => ({
    value: String(i + 1),
    label: name,
  }));

  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from({ length: currentYear - 1979 }, (_, i) => ({
    value: String(currentYear - i),
    label: String(currentYear - i),
  }));

  const modelOptions = ['Model 1', 'Model 2', 'Model 3'].map((m, i) => ({
    value: String(i + 1),
    label: m
  }));

  return (
    <FormProvider
      methods={methods}
      onSubmit={onSubmit}
      className="flex flex-1 gap-2 w-full"
    >
      <RHFDropdown fullWidth name="day" label="Day" options={dayOptions} />
      <RHFDropdown fullWidth name="month" label="Month" options={monthOptions} />
      <RHFDropdown fullWidth name="year" label="Year" options={yearOptions} />
      <RHFTextField name='latitude' label='Latitude' fullWidth />
      <RHFTextField name='longitude' label='Longitude' fullWidth />
      <RHFDropdown fullWidth name='model' label='Model' options={modelOptions} />

      <Button
        type='submit'
        variant='glass'
        className='self-end shrink-0 border border-transparent'
      >
        Submit
      </Button>
    </FormProvider>
  )
}