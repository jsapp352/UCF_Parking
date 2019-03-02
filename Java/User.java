// User.java
// Stephen Bennett

import java.util.ArrayList;

class User
{
	private static final int NUMBER_OF_GARAGES = 7;

	String name;
	String origin;
	String destination;
	ArrayList<String> preferred;

	User(String name)
	{
		this.name = name;
	}

	public String getName()
	{
		return name;
	}

	public void setName(String newName)
	{
		name = newName;
	}

	public String getOrigin()
	{
		return origin;
	}

	public void setOrigin(String newOrigin)
	{
		origin = newOrigin;
	}

	public String getDestination()
	{
		return destination;
	}

	public void setDestination(String newDestination)
	{
		destination = newDestination;
	}

	public void addPreferred(String garage)
	{
		preferred.add(garage);
	}

	public void removePreferred(String garage)
	{
		preferred.remove(garage);
	}

	public boolean isPreferred(String garage)
	{
		return preferred.contains(garage);
	}
}
