import imperial_materials_simulation as ims
import concurrent.futures as cf #Python standard multiprocessing library 

def sample_workflow(temperature: int) -> list[ims.Simulation, int]:
    #reduce size of simulation files by increasing the microstructure logging interval
    simulation = ims.Simulation(n_atoms=22, starting_temperature=temperature, microstructure_logging_interval=1_000)
    simulation.NVT_run(n_steps=100_000, temperature=temperature)
    simulation.MMC_run(n_steps=500_000, temperature=temperature)
    return simulation, temperature

if __name__ == '__main__':

    #only works in a .py file
    with cf.ProcessPoolExecutor() as executor:
        jobs = [executor.submit(sample_workflow, temperature) for temperature in range(100, 900, 100)]
        
        for job in cf.as_completed(jobs):
            simulation, temperature = job.result()
            print(f'simulation at {temperature}k finished')
            simulation.save(f'simulation {temperature}k') 